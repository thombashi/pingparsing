# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from collections import namedtuple
import ipaddress
import platform

import six
import typepy
from typepy.type import Integer

from ._logger import logger


DEFAULT_WAITTIME = 1


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

        Hostname or IP-address (IPv4/IPf6) to sending ICMP packets.

    .. py:attribute:: waittime

        Time ``[sec]`` of sending ICMP packets. This will be ignored if
        the value is ``None``. If both :py:attr:`~.waittime` and
        :py:attr:`~.count` are ``None``, :py:attr:`~.waittime` will be set to
        ``1``.
        Defaults to ``None``.

    .. py:attribute:: count

        Number of sending ICMP packets. This will be ignored if the value is
        ``None``. Defaults to ``None``.

    .. py:attribute:: ping_option

        Additional ``ping`` command option.

    .. py:attribute:: interface

        Interface name or zone-id. This will be required when
        :py:attr:`~.destination_host` is IPv6 link-local scope address.
        Defaults to ``None``.

    .. py:attribute:: auto_codepage

        [Only for windows environment] Automatically change code page if
        ``True``. Defaults to ``True``.
    """

    def __init__(self):
        self.destination_host = ""
        self.waittime = None
        self.count = None
        self.ping_option = ""
        self.interface = None
        self.auto_codepage = True

    def ping(self):
        """
        Sending ICMP packets.

        :return: ``ping`` command execution result.
        :rtype: :py:class:`.PingResult`
        :raises ValueError: If parameters not valid.
        """

        import subprocess

        self.__validate_ping_param()

        command_list = self.__get_base_ping_command_list()

        if typepy.is_not_null_string(self.ping_option):
            command_list.append(self.ping_option)

        command_list.extend([
            self.__get_waittime_option(),
            self.__get_count_option(),
        ])
        command = " ".join(command_list)

        logger.debug(command)

        ping_proc = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping_proc.communicate()

        return PingResult(stdout, stderr, ping_proc.returncode)

    def __is_windows(self):
        return platform.system() == "Windows"

    def __is_ipv6(self):
        try:
            network = ipaddress.ip_address(
                six.text_type(self.destination_host))
        except ValueError as e:
            logger.debug(e)
            return False

        logger.debug("IP address: version={}, address={}".format(
            network.version, self.destination_host))

        return network.version == 6

    def __validate_ping_param(self):
        if typepy.is_null_string(self.destination_host):
            raise ValueError("required destination_host")

        self.__validate_waittime()
        self.__validate_count()
        self.__validate_interface()

    def __validate_waittime(self):
        if self.waittime is None:
            return

        try:
            waittime = Integer(self.waittime).convert()
        except typepy.TypeConversionError:
            raise ValueError("wait time must be an integer: actual={}".format(
                self.waittime))

        if waittime <= 0:
            raise ValueError("wait time must be greater than zero")

    def __validate_count(self):
        if self.count is None:
            return

        try:
            count = Integer(self.count).convert()
        except typepy.TypeConversionError:
            raise ValueError("count must be an integer: actual={}".format(
                self.count))

        if count <= 0:
            raise ValueError("count must be greater than zero")

    def __validate_interface(self):
        if not self.__is_ipv6():
            return

        if not ipaddress.ip_network(
                six.text_type(self.destination_host)).is_link_local:
            return

        if typepy.is_null_string(self.interface):
            raise ValueError(
                "interface required to ping to IPv6 link local address")

    def __get_base_ping_command_list(self):
        command_list = []

        if self.__is_windows() and self.auto_codepage:
            command_list.append("chcp 437 &")

        command_list.extend([
            self.__get_ping_command(),
            self.__get_destination_host(),
        ])

        return command_list

    def __get_destination_host(self):
        if self.__is_windows() and self.__is_ipv6():
            return "{:s}%{}".format(self.destination_host, self.interface)

        return self.destination_host

    def __get_ping_command(self):
        if self.__is_windows():
            return "ping"

        if self.__is_ipv6():
            return "ping6"

        return "ping"

    def __get_waittime_option(self):
        try:
            waittime = Integer(self.waittime).convert()
        except typepy.TypeConversionError:
            if self.count:
                return ""

            waittime = DEFAULT_WAITTIME

        if self.__is_windows():
            return "-n {:d}".format(waittime)
        else:
            return "-q -w {:d}".format(waittime)

    def __get_count_option(self):
        try:
            count = Integer(self.count).convert()
        except typepy.TypeConversionError:
            return ""

        if self.__is_windows():
            return "-n {:d}".format(count)
        else:
            return "-c {:d}".format(count)
