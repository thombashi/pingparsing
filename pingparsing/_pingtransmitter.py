# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import ipaddress
import math
import platform
import warnings
from collections import namedtuple

import humanreadable as hr
import six
import subprocrunner
import typepy
from typepy import Integer, TypeConversionError

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


class PingTransmitter(object):
    """
    Transmitter class to send ICMP packets by using the OS built-in ``ping``
    command.

    .. py:attribute:: destination_host

        Hostname or IP-address (IPv4/IPv6) to sending ICMP packets.

    .. py:attribute:: count

        Number of sending ICMP packets. This attribute ignored if the value is
        |None|. Defaults to |None|.

    .. py:attribute:: ping_option

        Additional ``ping`` command option.

    .. py:attribute:: interface

        Interface name or zone-id. The attribute required when
        :py:attr:`~.destination_host` is IPv6 link-local scope address.
        Defaults to |None|.

    .. py:attribute:: auto_codepage

        [Only for Windows environment] Automatically change code page if
        ``True``. Defaults to ``True``.
    """

    @property
    def timeout(self):
        """
        Time to wait for a response per packet.
        You can specify either a number or a string (e.g. ``"1sec"``).
        If a number is specified, the unit will be considered as milliseconds.

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
    def timeout(self, value):
        if value is None:
            self.__timeout = value
            return

        timeout = hr.Time(str(value), default_unit=hr.Time.Unit.MILLISECOND)
        if timeout <= hr.Time("0s"):
            raise hr.ParameterError(
                "timeout is too low", expected="greater than zero", value=timeout
            )

        self.__timeout = timeout

    @property
    def deadline(self):
        """
        Timeout before ping exits.
        You can specify either a number or a string (e.g. ``"1sec"``).
        If both :py:attr:`~.deadline` and :py:attr:`~.count` are |None|,
        If a number is specified, the unit will be considered as seconds.

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

        if deadline <= hr.Time("0s"):
            raise hr.ParameterError(
                "deadline is too low", expected="greater than zero", value=deadline
            )

        self.__deadline = deadline

    @property
    def waittime(self):
        warnings.warn(
            "waittime will be deleted in the future, use deadline instead.", DeprecationWarning
        )

        return self.deadline

    @waittime.setter
    def waittime(self, value):
        warnings.warn(
            "waittime will be deleted in the future, use deadline instead.", DeprecationWarning
        )

        self.deadline = value

    def __init__(self):
        self.destination_host = ""
        self.count = None
        self.ping_option = ""
        self.is_quiet = False
        self.interface = None
        self.auto_codepage = True

        self.timeout = None
        self.deadline = None

    def ping(self):
        """
        Sending ICMP packets.

        :return: ``ping`` command execution result.
        :rtype: :py:class:`.PingResult`
        :raises ValueError: If parameters not valid.
        """

        self.__validate_ping_param()

        ping_proc = subprocrunner.SubprocessRunner(self.__get_ping_command())
        ping_proc.run()

        return PingResult(ping_proc.stdout, ping_proc.stderr, ping_proc.returncode)

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
            network = ipaddress.ip_address(six.text_type(self.destination_host))
        except ValueError as e:
            logger.debug(e)
            return False

        logger.debug(
            "IP address: version={}, address={}".format(network.version, self.destination_host)
        )

        return network.version == 6

    def __validate_ping_param(self):
        if typepy.is_null_string(self.destination_host):
            raise ValueError("required destination_host")

        self.__validate_count()
        self.__validate_interface()

    def __validate_count(self):
        if self.count is None:
            return

        try:
            count = Integer(self.count).convert()
        except TypeConversionError as e:
            raise ValueError("count must be an integer: {}".format(e))

        if count <= 0:
            raise ValueError("count must be greater than zero")

    def __validate_interface(self):
        if not self.__is_ipv6():
            return

        if not ipaddress.ip_network(six.text_type(self.destination_host)).is_link_local:
            return

        if typepy.is_null_string(self.interface):
            raise ValueError("interface required to ping to IPv6 link local address")

    def __get_ping_command(self):
        command_list = []

        if self.__is_windows() and self.auto_codepage:
            command_list.append("chcp 437 &")

        command_list.extend(
            [
                self.__get_builtin_ping_command(),
                self.__get_deadline_option(),
                self.__get_timeout_option(),
                self.__get_count_option(),
                self.__get_quiet_option(),
            ]
        )

        if self.__is_linux() and typepy.is_not_null_string(self.interface):
            command_list.append("-I {}".format(self.interface))

        if typepy.is_not_null_string(self.ping_option):
            command_list.append(self.ping_option)

        command_list.append(self.__get_destination_host())

        return " ".join(command_list)

    def __get_destination_host(self):
        if self.__is_windows() and self.__is_ipv6():
            return "{:s}%{}".format(self.destination_host, self.interface)

        return self.destination_host

    def __get_builtin_ping_command(self):
        if self.__is_windows():
            return "ping"

        if self.__is_ipv6():
            return "ping6"

        return "ping"

    def __get_quiet_option(self):
        if not self.is_quiet or self.__is_windows():
            return ""

        return "-q"

    def __get_deadline_option(self):
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

    def __get_timeout_option(self):
        if self.timeout is None:
            return ""

        if self.__is_linux():
            # timeout option value accept in seconds in Linux ping and float values
            # not accepted.
            return "-W {:d}".format(int(math.ceil(self.timeout.seconds)))
        if self.__is_windows():
            return "-w {:d}".format(int(math.ceil(self.timeout.milliseconds)))

        return ""

    def __get_count_option(self):
        try:
            count = Integer(self.count).convert()
        except TypeConversionError:
            return ""

        if self.__is_windows():
            return "-n {:d}".format(count)

        return "-c {:d}".format(count)
