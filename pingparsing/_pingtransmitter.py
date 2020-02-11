"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import ipaddress
import math
import platform
import re
from collections import namedtuple
from typing import Optional, cast

import humanreadable as hr
import subprocrunner
import typepy
from typepy import Integer, StrictLevel, String, TypeConversionError

from ._logger import logger


DEFAULT_DEADLINE = 3


class PingResult(namedtuple("PingResult", "stdout stderr returncode")):
    """
    Data class to store ``ping`` command execution result.

    .. py:attribute:: stdout

        Standard output of ``ping`` command execution result.

    .. py:attribute:: stderr

        Standard error of ``ping`` command execution result.

    .. py:attribute:: returncode

        Return code of ``ping`` command execution result.
    """


class PingTransmitter:
    """
    Transmitter class to send ICMP packets by using the OS built-in ``ping``
    command.

    .. py:attribute:: count

        Number of sending ICMP packets. This attribute ignored if the value is
        |None|. Defaults to |None|.

    .. py:attribute:: ping_option

        Additional ``ping`` command option.

    .. py:attribute:: interface

        Interface name or zone-id. The attribute required when
        :py:attr:`~.destination` is IPv6 link-local scope address.
        Defaults to |None|.

    .. py:attribute:: timestamp

        [Only for Linux environment] If |True|, add timestamp for each ping result.
        Defaults to ``False``.

    .. py:attribute:: auto_codepage

        [Only for Windows environment] Automatically change code page if
        ``True``. Defaults to ``True``.
    """

    @property
    def destination(self) -> str:
        """
        Hostname or IP-address (IPv4/IPv6) to sending ICMP packets.
        """

        return self.__destination

    @destination.setter
    def destination(self, value: str) -> None:
        if not String(value, strict_level=StrictLevel.MAX).is_type():
            raise ValueError("empty destination")

        self.__destination = value

    @property
    def destination_host(self) -> str:
        """
        Alias to :py:attr:`~.destination`
        """

        return self.destination

    @destination_host.setter
    def destination_host(self, value: str) -> None:
        self.destination = value

    @property
    def timeout(self) -> Optional[hr.Time]:
        """
        Time to wait for a response per packet.
        You can specify either a number or a string (e.g. ``"1sec"``).
        If only a number is specified and a unit not found, the unit will be considered as seconds.

            +------------+----------------------------------------------------------+
            |    Unit    |                Available specifiers (str)                |
            +============+==========================================================+
            |days        |``d``/``day``/``days``                                    |
            +------------+----------------------------------------------------------+
            |hours       |``h``/``hour``/``hours``                                  |
            +------------+----------------------------------------------------------+
            |minutes     |``m``/``min``/``mins``/``minute``/``minutes``             |
            +------------+----------------------------------------------------------+
            |seconds     |``s``/``sec``/``secs``/``second``/``seconds``             |
            +------------+----------------------------------------------------------+
            |milliseconds|``ms``/``msec``/``msecs``/``millisecond``/``milliseconds``|
            +------------+----------------------------------------------------------+
            |microseconds|``us``/``usec``/``usecs``/``microsecond``/``microseconds``|
            +------------+----------------------------------------------------------+

        Use system default timeout if the value is |None|.
        Defaults to |None|.
        If the system does not support timeout in milliseconds, round up as seconds.

        Returns:
            humanreadable.Time: timeout
        """

        return self.__timeout

    @timeout.setter
    def timeout(self, value: Optional[str]):
        if value is None:
            self.__timeout = value  # type: Optional[hr.Time]
            return

        timeout = hr.Time(str(value), default_unit=hr.Time.Unit.MILLISECOND)
        if timeout.milliseconds <= 0:
            raise ValueError("timeout must be greater than zero")

        self.__timeout = cast(hr.Time, timeout)

    @property
    def deadline(self):
        """
        Timeout before ping exits.
        You can specify either a number or a string (e.g. ``"1sec"``).
        If both :py:attr:`~.deadline` and :py:attr:`~.count` are |None|,
        If only a number is specified and a unit not found, the unit will be considered as seconds.

            +------------+----------------------------------------------------------+
            |    Unit    |                Available specifiers (str)                |
            +============+==========================================================+
            |days        |``d``/``day``/``days``                                    |
            +------------+----------------------------------------------------------+
            |hours       |``h``/``hour``/``hours``                                  |
            +------------+----------------------------------------------------------+
            |minutes     |``m``/``min``/``mins``/``minute``/``minutes``             |
            +------------+----------------------------------------------------------+
            |seconds     |``s``/``sec``/``secs``/``second``/``seconds``             |
            +------------+----------------------------------------------------------+
            |milliseconds|``ms``/``msec``/``msecs``/``millisecond``/``milliseconds``|
            +------------+----------------------------------------------------------+
            |microseconds|``us``/``usec``/``usecs``/``microsecond``/``microseconds``|
            +------------+----------------------------------------------------------+

        :py:attr:`~.deadline` automatically set to the default value (``3 seconds``).
        Defaults to |None|.

        Returns:
            humanreadable.Time: deadline
        """

        return self.__deadline

    @deadline.setter
    def deadline(self, value):
        if value is None:
            self.__deadline = value
            return

        deadline = hr.Time(str(value), default_unit=hr.Time.Unit.SECOND)

        if deadline.milliseconds <= 0:
            raise ValueError("deadline must be greater than zero")

        self.__deadline = deadline

    def __init__(self) -> None:
        self.__destination = ""
        self.count = None
        self.ping_option = ""
        self.is_quiet = False
        self.interface = None
        self.auto_codepage = True

        self.timeout = None
        self.deadline = None
        self.timestamp = False

    def ping(self) -> PingResult:
        """
        Sending ICMP packets.

        :return: ``ping`` command execution result.
        :rtype: :py:class:`.PingResult`
        :raises ValueError: If parameters not valid.
        """

        self.__validate_ping_param()

        ping_runner = subprocrunner.SubprocessRunner(self.__get_ping_command())
        ping_runner.run()

        return PingResult(ping_runner.stdout, ping_runner.stderr, ping_runner.returncode)

    @staticmethod
    def __is_linux():
        return platform.system() == "Linux"

    @staticmethod
    def __is_macos():
        return platform.system() == "Darwin"

    @staticmethod
    def __is_windows():
        return platform.system() == "Windows"

    def __is_ipv6(self):
        try:
            network = ipaddress.ip_address(str(self.destination))
        except ValueError as e:
            logger.debug(e)
            return False

        logger.debug("IP address: version={}, address={}".format(network.version, self.destination))

        return network.version == 6

    def __validate_ping_param(self) -> None:
        self.__validate_count()
        self.__validate_interface()

    def __validate_count(self) -> None:
        if self.count is None:
            return

        try:
            count = Integer(self.count).convert()
        except TypeConversionError as e:
            raise ValueError("count must be an integer: {}".format(e))

        if count <= 0:
            raise ValueError("count must be greater than zero")

    def __validate_interface(self) -> None:
        if not self.__is_ipv6():
            return

        if not ipaddress.ip_network(str(self.destination)).is_link_local:
            return

        if typepy.is_null_string(self.interface):
            raise ValueError("interface required to ping to IPv6 link local address")

    def __get_ping_command(self) -> str:
        command_items = []

        if self.__is_windows() and self.auto_codepage:
            command_items.append("chcp 437 &")

        command_items.extend(
            [
                self.__get_builtin_ping_command(),
                self.__get_deadline_option(),
                self.__get_timeout_option(),
                self.__get_count_option(),
                self.__get_timestamp_option(),
                self.__get_quiet_option(),
            ]
        )

        if self.__is_linux() and typepy.is_not_null_string(self.interface):
            command_items.append("-I {}".format(self.interface))

        if typepy.is_not_null_string(self.ping_option):
            command_items.append(self.ping_option)

        command_items.append(self.__get_destination_host())

        return re.sub(r"[\s]{2,}", " ", " ".join(command_items))

    def __get_destination_host(self) -> str:
        if self.__is_windows() and self.__is_ipv6():
            return "{:s}%{}".format(self.destination, self.interface)

        return self.destination

    def __get_builtin_ping_command(self) -> str:
        if self.__is_windows():
            return "ping"

        if self.__is_ipv6():
            return "ping6"

        return "ping"

    def __get_quiet_option(self) -> str:
        if not self.is_quiet or self.__is_windows():
            return ""

        return "-q"

    def __get_timestamp_option(self) -> str:
        if not self.timestamp or self.__is_windows():
            return ""

        return "-D"

    def __get_deadline_option(self) -> str:
        if self.deadline is None:
            if self.count:
                return ""

            deadline = DEFAULT_DEADLINE
        else:
            deadline = int(math.ceil(self.deadline.seconds))

        if self.__is_windows():
            # ping for Windows does not have the option with equals to the deadline option.
            return "-n {:d}".format(deadline)
        elif self.__is_macos():
            if self.__is_ipv6():
                # there is no timeout option for macOS ping6.
                # so, using -i and -c option to simulate timeout.
                return "-i 1 -c {:d}".format(deadline)

            return "-t {:d}".format(deadline)

        return "-w {:d}".format(deadline)

    def __get_timeout_option(self) -> str:
        if self.timeout is None:
            return ""

        if self.__is_linux():
            # timeout option value accept in seconds in Linux ping and float values
            # not accepted.
            return "-W {:d}".format(int(math.ceil(self.timeout.seconds)))
        if self.__is_windows():
            return "-w {:d}".format(int(math.ceil(self.timeout.milliseconds)))

        return ""

    def __get_count_option(self) -> str:
        try:
            count = Integer(self.count).convert()
        except TypeConversionError:
            return ""

        if self.__is_windows():
            return "-n {:d}".format(count)

        return "-c {:d}".format(count)
