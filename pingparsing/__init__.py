#!/usr/bin/env python

'''
@author: Tsuyoshi Hombashi
'''

import platform
import re

import dataproperty
import pyparsing as pp


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
            command_list.append("-n %d" % (self.waittime))
        else:
            command_list.append("-q -w %d" % (self.waittime))

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


class PingParsing(object):

    def __init__(self):
        self.destination_host = ""
        self.waittime = 1
        self.ping_option = ""

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

    def parse(self, ping_message):
        self.__initialize_parse_result()

        if dataproperty.is_empty_string(ping_message):
            return

        try:
            self.__parse_linux_ping(ping_message)
            return
        except ValueError:
            pass

        self.__parse_windows_ping(ping_message)

    def __parse_windows_ping(self, ping_message):
        line_list = ping_message.splitlines()

        for i, line in enumerate(line_list):
            if re.search("^Ping statistics for ", line):
                break
        else:
            raise ValueError("can not parse")

        packet_line = line_list[i + 1].strip()
        rtt_line = line_list[i + 3].strip()

        packet_pattern = (
            pp.Literal("Packets: Sent = ") +
            pp.Word(pp.nums) +
            pp.Literal(", Received = ") +
            pp.Word(pp.nums) +
            pp.Literal(", Lost = ") +
            pp.Word(pp.nums) + "(" +
            pp.Word(pp.nums + ".")
        )
        parse_list = packet_pattern.parseString(packet_line)
        self.__packet_transmit = int(parse_list[1])
        self.__packet_receive = int(parse_list[3])
        self.__packet_loss = float(parse_list[7])

        rtt_pattern = (
            pp.Literal("Minimum = ") +
            pp.Word(pp.nums) +
            pp.Literal("ms, Maximum = ") +
            pp.Word(pp.nums) +
            pp.Literal("ms, Average = ") +
            pp.Word(pp.nums)
        )
        parse_list = rtt_pattern.parseString(rtt_line)
        self.__rtt_min = float(parse_list[1])
        self.__rtt_avg = float(parse_list[5])
        self.__rtt_max = float(parse_list[3])

    def __parse_linux_ping(self, ping_message):
        line_list = ping_message.splitlines()

        for i, line in enumerate(line_list):
            if re.search("--- .* ping statistics ---", line):
                break
        else:
            raise ValueError("can not parse")

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
