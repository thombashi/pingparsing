# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple
import platform

import dataproperty


PingResult = namedtuple("PingResult", "stdout stderr returncode")


class PingTransmitter(object):

    def __init__(self):
        self.destination_host = ""
        self.waittime = 1
        self.ping_option = ""

    def ping(self):
        import subprocess

        self.__validate_ping_param()

        command_list = [
            "ping",
            self.destination_host,
        ]

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
            raise ValueError("destination_host host is empty")

        if self.waittime <= 0:
            raise ValueError(
                "wait time expected to be greater than or equal to zero")
