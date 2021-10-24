"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import ipaddress
import platform
from collections import namedtuple
from typing import Optional, cast

import humanreadable as hr
import subprocrunner
import typepy
from subprocrunner.typing import Command
from typepy import Integer, StrictLevel, String, TypeConversionError

from ._cmd_maker import LinuxPingCmdMaker, MacosPingCmdMaker, WindowsPingCmdMaker
from ._logger import logger
from ._typing import PingAddOpts, TimeArg


DEFAULT_DEADLINE = 3


class PingResult(namedtuple("PingResult", "stdout stderr returncode")):
    """
    Data class to store ``ping`` command execution result.

    .. py:attribute:: stdout
        :type: Optional[str]

        Standard output of ``ping`` command execution result.

    .. py:attribute:: stderr
        :type: Optional[str]

        Standard error of ``ping`` command execution result.

    .. py:attribute:: returncode
        :type: int

        Return code of ``ping`` command execution result.
    """


class PingTransmitter:
    """
    Transmitter class to send ICMP packets by using the OS built-in ``ping``
    command.

    .. py:attribute:: count
        :type: Optional[int]
        :value: None

        Number of sending ICMP packets. This attribute ignored if the value is |None|.

    .. py:attribute:: packet_size
        :type: Optional[int]
        :value: None

        Specifies the number of data bytes to be sent.

    .. py:attribute:: ttl
        :type: Optional[int]
        :value: None

        Specifies the Time to Live.

    .. py:attribute:: ping_option
        :type: Union[str, Sequence[str]]
        :value: ""

        Additional ``ping`` command option.

    .. py:attribute:: interface
        :type: Optional[str]
        :value: None

        Interface name or zone-id. The attribute required when
        :py:attr:`~.destination` is IPv6 link-local scope address.

    .. py:attribute:: timestamp
        :type: bool
        :value: False

        [Only for Linux environment] If |True|, add timestamp for each ping result.
        Defaults to ``False``.

    .. py:attribute:: auto_codepage
        :type: bool
        :value: True

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
    def timeout(self, value: TimeArg) -> None:
        if value is None:
            self.__timeout: Optional[hr.Time] = value
            return

        if isinstance(value, hr.Time):
            timeout = cast(hr.Time, value)
        else:
            timeout = hr.Time(str(value), default_unit=hr.Time.Unit.MILLISECOND)

        if timeout.milliseconds <= 0:
            raise ValueError("timeout must be greater than zero")

        self.__timeout = cast(hr.Time, timeout)

    @property
    def deadline(self) -> Optional[hr.Time]:
        """
        Timeout before ping exits.
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

        If both :py:attr:`~.deadline` and :py:attr:`~.count` are |None|,
        :py:attr:`~.deadline` is automatically set to the default value (``3 seconds``).
        Defaults to |None|.

        Returns:
            humanreadable.Time: deadline
        """

        return self.__deadline

    @deadline.setter
    def deadline(self, value: TimeArg) -> None:
        if value is None:
            self.__deadline = value
            return

        if isinstance(value, hr.Time):
            deadline = cast(hr.Time, value)
        else:
            deadline = hr.Time(str(value), default_unit=hr.Time.Unit.SECOND)

        if deadline.milliseconds <= 0:
            raise ValueError("deadline must be greater than zero")

        self.__deadline = deadline

    def __init__(self) -> None:
        self.__destination = ""
        self.count: Optional[int] = None
        self.packet_size: Optional[int] = None
        self.ttl: Optional[int] = None
        self.ping_option: PingAddOpts = []
        self.is_quiet = False
        self.interface: Optional[str] = None
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

        ping_runner = subprocrunner.SubprocessRunner(self.__make_ping_command())
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

        logger.debug(f"IP address: version={network.version}, address={self.destination}")

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
            raise ValueError(f"count must be an integer: {e}")

        if count <= 0:
            raise ValueError("count must be greater than zero")

    def __validate_interface(self) -> None:
        if not self.__is_ipv6():
            return

        if not ipaddress.ip_network(str(self.destination)).is_link_local:
            return

        if typepy.is_null_string(self.interface):
            raise ValueError("interface required to ping to IPv6 link local address")

    def __make_ping_command(self) -> Command:
        from typing import Any  # noqa

        maker_class: Any = None

        if self.__is_linux():
            maker_class = LinuxPingCmdMaker
        elif self.__is_macos():
            maker_class = MacosPingCmdMaker
        elif self.__is_windows():
            maker_class = WindowsPingCmdMaker
        else:
            raise RuntimeError(f"not supported platform: {platform.system()}")

        return maker_class(
            count=self.count,
            packet_size=self.packet_size,
            ttl=self.ttl,
            deadline=self.deadline,
            timeout=self.timeout,
            interface=self.interface,
            is_ipv6=self.__is_ipv6(),
            timestamp=self.timestamp,
            auto_codepage=self.auto_codepage,
            ping_option=self.ping_option,
        ).make_cmd(destination=self.destination)
