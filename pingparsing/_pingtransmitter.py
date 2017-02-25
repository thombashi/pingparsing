# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple
import platform

import typepy
from typepy.type import Integer


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

        Hostname/IP-address to sending ICMP packets.

    .. py:attribute:: waittime

        Time [sec] for sending packets.
        If the value is ``None``, sending packets time will be the same as
        built-in ``ping`` command.
        Defaults to 1 [sec].

    .. py:attribute:: count

        Number of sending ICMP packets.
        The value will be ignored if the value is ``None``.
        Defaults to ``None``.

    .. py:attribute:: ping_option

        Additional ``ping`` command option.

    .. py:attribute:: auto_codepage

        [Only for windows environment] Automatically change code page if
        ``True``. Defaults to ``True``.
    """

    def __init__(self):
        self.destination_host = ""
        self.waittime = 1
        self.count = None
        self.ping_option = ""
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

        command_list = self.__get_base_ping_command()

        if typepy.is_not_null_string(self.ping_option):
            command_list.append(self.ping_option)

        command_list.append(self.__get_waittime_option())
        command_list.append(self.__get_count_option())

        ping_proc = subprocess.Popen(
            " ".join(command_list), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping_proc.communicate()

        return PingResult(stdout, stderr, ping_proc.returncode)

    def __validate_ping_param(self):
        if typepy.is_null_string(self.destination_host):
            raise ValueError("required destination_host")

        self.__validate_waittime()
        self.__validate_count()

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

    def __get_base_ping_command(self):
        command_list = []

        if platform.system() == "Windows" and self.auto_codepage:
            command_list.append("chcp 437 &")

        command_list.extend([
            "ping",
            self.destination_host,
        ])

        return command_list

    def __get_waittime_option(self):
        try:
            waittime = Integer(self.waittime).convert()
        except typepy.TypeConversionError:
            return ""

        if platform.system() == "Windows":
            return "-n {:d}".format(waittime)
        else:
            return "-q -w {:d}".format(waittime)

    def __get_count_option(self):
        try:
            count = Integer(self.count).convert()
        except typepy.TypeConversionError:
            return ""

        if platform.system() == "Windows":
            return "-n {:d}".format(count)
        else:
            return "-c {:d}".format(count)
