# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple
import platform

import dataproperty


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
    Transmitter class to send ICMP packets by using the built-in ``ping``
    command.

    .. py:attribute:: destination_host

        Hostname/IP-address to sending ICMP packets.

    .. py:attribute:: waittime

        Time [sec] for sending packets.
        Defaults to 1 [sec].

    .. py:attribute:: ping_option

        Additional ``ping`` command option.

    .. py:attribute:: auto_codepage

        Automatically change code page if ``True``.
        Defaults to ``True``.
    """

    def __init__(self):
        self.destination_host = ""
        self.waittime = 1
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

        if dataproperty.is_not_empty_string(self.ping_option):
            command_list.append(self.ping_option)

        if platform.system() == "Windows":
            command_list.append("-n {:d}".format(self.waittime))
        else:
            command_list.append("-q -w {:d}".format(self.waittime))

        ping_proc = subprocess.Popen(
            " ".join(command_list), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping_proc.communicate()

        return PingResult(stdout, stderr, ping_proc.returncode)

    def __validate_ping_param(self):
        if dataproperty.is_empty_string(self.destination_host):
            raise ValueError("required destination_host")

        if self.waittime <= 0:
            raise ValueError(
                "wait time must be greater than or equal to zero")

    def __get_base_ping_command(self):
        command_list = []

        if platform.system() == "Windows" and self.auto_codepage:
            command_list.append("chcp 437 &")

        command_list.extend([
            "ping",
            self.destination_host,
        ])

        return command_list
