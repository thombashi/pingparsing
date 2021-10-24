import abc
import math
from typing import List, Optional

import humanreadable as hr
from subprocrunner.typing import Command
from typepy import Integer

from ._typing import PingAddOpts


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
        ping_option: PingAddOpts = "",
    ):
        self.count = count
        if self.count is not None:
            self.count = Integer(self.count).convert()

        self.deadline = deadline
        self.timeout = timeout
        self._packet_size = packet_size
        self._ttl = ttl
        self.interface = interface
        self._is_ipv6 = is_ipv6
        self._timestamp = timestamp
        self.auto_codepage = auto_codepage
        self.ping_option = ping_option

    def make_cmd(self, destination: str) -> Command:
        command_items = (
            self._get_initial_command()
            + self._get_ping_command()
            + self._get_interface_option()
            + self._get_deadline_option()
            + self._get_timeout_option()
            + self._get_count_option()
            + self._get_packet_size_option()
            + self._get_ttl_option()
        )

        if self._timestamp:
            command_items.extend(self._get_timestamp_option())

        if isinstance(self.ping_option, str):
            command_items.extend(self.ping_option.strip().split())
        else:
            command_items.extend(self.ping_option)

        command_items.append(self._get_destination_host(destination))

        if self._require_shell_command():
            return " ".join(command_items)

        return command_items

    def _get_initial_command(self) -> List[str]:
        return []

    @abc.abstractmethod
    def _get_destination_host(self, destination: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_ping_command(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_quiet_option(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_timestamp_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_deadline_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_timeout_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_count_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_packet_size_option(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_ttl_option(self) -> List[str]:
        raise NotImplementedError()

    def _get_interface_option(self) -> List[str]:
        return []

    def _require_shell_command(self) -> bool:
        return False


class PosixPingCmdMaker(PingCmdMaker):
    def _get_destination_host(self, destination: str) -> str:
        return destination

    def _get_ping_command(self) -> List[str]:
        if self._is_ipv6:
            return ["ping6"]

        return ["ping"]

    def _get_quiet_option(self) -> str:
        return "-q"

    def _get_timestamp_option(self) -> List[str]:
        return ["-D", "-O"]

    def _get_count_option(self) -> List[str]:
        if self.count is None:
            return []

        return ["-c", str(self.count)]

    def _get_packet_size_option(self) -> List[str]:
        if self._packet_size is None:
            return []

        return ["-s", str(self._packet_size)]


class MacosPingCmdMaker(PosixPingCmdMaker):
    def _get_ttl_option(self) -> List[str]:
        if self._ttl is None:
            return []

        return ["-T", str(self._ttl)]

    def _get_deadline_option(self) -> List[str]:
        if self.deadline is None:
            if self.count:
                return []

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        if self._is_ipv6:
            # there is no timeout option for macOS ping6.
            # so, using -i and -c option to simulate timeout.
            return ["-i", "1", "-c", str(deadline)]

        return ["-t", str(deadline)]

    def _get_timeout_option(self) -> List[str]:
        return []


class LinuxPingCmdMaker(PosixPingCmdMaker):
    def _get_ttl_option(self) -> List[str]:
        if self._ttl is None:
            return []

        return ["-t", str(self._ttl)]

    def _get_deadline_option(self) -> List[str]:
        if self.deadline is None:
            if self.count:
                return []

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        return ["-w", str(deadline)]

    def _get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []

        return ["-W", str(int(math.ceil(self.timeout.seconds)))]

    def _get_interface_option(self) -> List[str]:
        if not self.interface:
            return []

        return ["-I", self.interface]


class WindowsPingCmdMaker(PingCmdMaker):
    def _get_initial_command(self) -> List[str]:
        if self.auto_codepage:
            return ["chcp 437 &"]

        return []

    def _get_destination_host(self, destination: str) -> str:
        if self._is_ipv6:
            return f"{destination:s}%{self.interface}"

        return destination

    def _get_ping_command(self) -> List[str]:
        return ["ping"]

    def _get_quiet_option(self) -> str:
        return ""

    def _get_timestamp_option(self) -> List[str]:
        return []

    def _get_deadline_option(self) -> List[str]:
        if self.deadline is None:
            if self.count:
                return []

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        # ping for Windows does not have the option with equals to the deadline option.
        return ["-n", str(deadline)]

    def _get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []

        return ["-w", str(int(math.ceil(self.timeout.milliseconds)))]

    def _get_count_option(self) -> List[str]:
        if self.count is None:
            return []

        return ["-n", str(self.count)]

    def _get_packet_size_option(self) -> List[str]:
        if self._packet_size is None:
            return []

        return ["-l", str(self._packet_size)]

    def _get_ttl_option(self) -> List[str]:
        if self._ttl is None:
            return []

        return ["-i", str(self._ttl)]

    def _require_shell_command(self) -> bool:
        return self.auto_codepage
