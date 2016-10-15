# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import platform

import dataproperty


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

        if ping_proc.returncode != 0:
            raise RuntimeError(stderr)

        return stdout

    def __validate_ping_param(self):
        if dataproperty.is_empty_string(self.destination_host):
            raise ValueError("destination_host host is empty")

        if self.waittime <= 0:
            raise ValueError(
                "waittime expected to be greater than or equal to zero")
