import abc
import math
import re
from typing import List, Optional

import humanreadable as hr
from typepy import Integer, TypeConversionError


DEFAULT_DEADLINE = 3


class PingCmdMaker(metaclass=abc.ABCMeta):
    def __init__(
        self,
        count: Optional[int] = None,
        deadline: Optional[hr.Time] = None,
        timeout: Optional[hr.Time] = None,
        packet_size: Optional[int] = None,
        ttl: Optional[int] = None,
        interface: Optional[str] = None,
        is_ipv6: bool = False,
        timestamp: bool = False,
        auto_codepage: bool = False,
        ping_option: Optional[str] = None,
    ):
        self.count = count
        self.deadline = deadline
        self.timeout = timeout
        self._packet_size = packet_size
        self._ttl = ttl
        self.interface = interface
        self._is_ipv6 = is_ipv6
        self._timestamp = timestamp
        self.auto_codepage = auto_codepage
        self.ping_option = ping_option

    def make_cmd(self, destination: str) -> str:
        command_items = self._get_initial_options()
        command_items.extend(
            [
                self._get_builtin_ping_command(),
                self._get_deadline_option(),
                self._get_timeout_option(),
                self._get_count_option(),
            ]
        )

        if self._packet_size:
            command_items.extend(self._get_packet_size_option())

        if self._ttl:
            command_items.extend(self._get_ttl_option())

        if self._timestamp:
            command_items.append(self._get_timestamp_option())

        if self.ping_option:
            command_items.append(self.ping_option)

        command_items.append(self._get_destination_host(destination))

        return re.sub(r"[\s]{2,}", " ", " ".join(command_items))

    def _get_initial_options(self) -> List[str]:
        return []

    @abc.abstractmethod
    def _get_destination_host(self, destination: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_builtin_ping_command(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_quiet_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_timestamp_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_deadline_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_timeout_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_count_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_packet_size_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_ttl_option(self) -> List[str]:
        raise NotImplementedError()


class PosixPingCmdMaker(PingCmdMaker):
    def _get_destination_host(self, destination: str) -> str:
        return destination

    def _get_builtin_ping_command(self) -> str:
        if self._is_ipv6:
            return "ping6"

        return "ping"

    def _get_quiet_option(self) -> str:
        return "-q"

    def _get_timestamp_option(self) -> str:
        return "-D"

    def _get_count_option(self) -> str:
        try:
            count = Integer(self.count).convert()
        except TypeConversionError:
            return ""

        return "-c {:d}".format(count)

    def _get_packet_size_option(self) -> List[str]:
        return ["-s", str(self._packet_size)]


class MacosPingCmdMaker(PosixPingCmdMaker):
    def _get_ttl_option(self) -> List[str]:
        return ["-T", str(self._ttl)]

    def _get_deadline_option(self) -> str:
        if self.deadline is None:
            if self.count:
                return ""

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        if self._is_ipv6:
            # there is no timeout option for macOS ping6.
            # so, using -i and -c option to simulate timeout.
            return "-i 1 -c {:d}".format(deadline)

        return "-t {:d}".format(deadline)

    def _get_timeout_option(self) -> str:
        return ""


class LinuxPingCmdMaker(PosixPingCmdMaker):
    def _get_ttl_option(self) -> List[str]:
        return ["-t", str(self._ttl)]

    def _get_deadline_option(self) -> str:
        if self.deadline is None:
            if self.count:
                return ""

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        return "-w {:d}".format(deadline)

    def _get_timeout_option(self) -> str:
        if self.timeout is None:
            return ""

        return "-W {:d}".format(int(math.ceil(self.timeout.seconds)))


class WindowsPingCmdMaker(PingCmdMaker):
    def _get_initial_options(self) -> List[str]:
        if self.auto_codepage:
            return ["chcp 437 &"]

        return []

    def _get_destination_host(self, destination: str) -> str:
        if self._is_ipv6:
            return "{:s}%{}".format(destination, self.interface)

        return destination

    def _get_builtin_ping_command(self) -> str:
        return "ping"

    def _get_quiet_option(self) -> str:
        return ""

    def _get_timestamp_option(self) -> str:
        return ""

    def _get_deadline_option(self) -> str:
        if self.deadline is None:
            if self.count:
                return ""

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        # ping for Windows does not have the option with equals to the deadline option.
        return "-n {:d}".format(deadline)

    def _get_timeout_option(self) -> str:
        if self.timeout is None:
            return ""

        return "-w {:d}".format(int(math.ceil(self.timeout.milliseconds)))

    def _get_count_option(self) -> str:
        try:
            count = Integer(self.count).convert()
        except TypeConversionError:
            return ""

        return "-n {:d}".format(count)

    def _get_packet_size_option(self) -> List[str]:
        return ["-l", str(self._packet_size)]

    def _get_ttl_option(self) -> List[str]:
        return ["-i", str(self._ttl)]
