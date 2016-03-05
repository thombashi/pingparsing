#!/usr/bin/env python

'''
@author: Tsuyoshi Hombashi
'''

import re

import dataproperty
import pyparsing as pp


class PingParsing(object):

    def __init__(self):
        self.destination_host = ""
        self.waittime = 1
        self.extra_option = ""

        self.__initialize_parse_result()

    @property
    def packet_transmit(self):
        return self.__packet_transmit

    @property
    def packet_receive(self):
        return self.__packet_receive

    @property
    def packet_loss(self):
        return self.__packet_loss

    @property
    def rtt_min(self):
        return self.__rtt_min

    @property
    def rtt_avg(self):
        return self.__rtt_avg

    @property
    def rtt_max(self):
        return self.__rtt_max

    @property
    def rtt_mdev(self):
        return self.__rtt_mdev

    def as_dict(self):
        return {
            "packet_transmit": self.packet_transmit,
            "packet_receive": self.packet_receive,
            "packet_loss": self.packet_loss,
            "rtt_min": self.rtt_min,
            "rtt_avg": self.rtt_avg,
            "rtt_max": self.rtt_max,
            "rtt_mdev": self.rtt_mdev,
        }

    def ping(self):
        import subprocess

        self.__validate_ping_param()

        command_list = [
            "ping",
            self.destination_host,
            "-f -q",
            "-w %d" % (self.waittime),
        ]
        if dataproperty.is_not_empty_string(self.extra_option):
            command_list.append(self.extra_option)

        ping_proc = subprocess.Popen(
            " ".join(command_list), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping_proc.communicate()

        if ping_proc.returncode != 0:
            raise RuntimeError(stderr)

        return stdout

    def parse(self, ping_message):
        self.__initialize_parse_result()

        if dataproperty.is_empty_string(ping_message):
            return

        line_list = ping_message.splitlines()
        for i, line in enumerate(line_list):
            if re.search("--- .* ping statistics ---", line):
                break

        packet_line, rtt_line = line_list[i + 1:]

        packet_pattern = (
            pp.Word(pp.nums) +
            pp.Literal("packets transmitted,") +
            pp.Word(pp.nums) +
            pp.Literal("received,") +
            pp.Word(pp.nums + ".") +
            pp.Literal("% packet loss")
        )
        parse_list = packet_pattern.parseString(packet_line)
        self.__packet_transmit = int(parse_list[0])
        self.__packet_receive = int(parse_list[2])
        self.__packet_loss = float(parse_list[4])

        rtt_pattern = (
            pp.Literal("rtt min/avg/max/mdev =") +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") +
            pp.Word(pp.nums + "ms")
        )
        parse_list = rtt_pattern.parseString(rtt_line)

        self.__rtt_min = float(parse_list[1])
        self.__rtt_avg = float(parse_list[3])
        self.__rtt_max = float(parse_list[5])
        self.__rtt_mdev = float(parse_list[7])

    def __initialize_parse_result(self):
        self.__packet_transmit = None
        self.__packet_receive = None
        self.__packet_loss = None
        self.__rtt_min = None
        self.__rtt_avg = None
        self.__rtt_max = None
        self.__rtt_mdev = None

    def __validate_ping_param(self):
        if dataproperty.is_empty_string(self.destination_host):
            raise ValueError("destination_host host is empty")

        if self.waittime <= 0:
            raise ValueError(
                "waittime expected to be greater than or equal to zero")
