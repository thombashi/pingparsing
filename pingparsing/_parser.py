# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import division

import re

import typepy

import pyparsing as pp

from ._interface import PingParserInterface
from ._logger import logger
from .error import EmptyPingStaticticsError
from .error import PingStaticticsHeaderNotFoundError


def _to_unicode(text):
    try:
        return text.decode("ascii")
    except AttributeError:
        return text


class PingParser(PingParserInterface):

    def __init__(self):
        self.ping_option = ""

        self._initialize_parse_result()

    @property
    def packet_transmit(self):
        return self._packet_transmit

    @property
    def packet_receive(self):
        return self._packet_receive

    @property
    def packet_loss_rate(self):
        try:
            return (1.0 - (self.packet_receive / self.packet_transmit)) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def packet_loss_count(self):
        try:
            return self.packet_transmit - self.packet_receive
        except TypeError:
            return None

    @property
    def rtt_min(self):
        return self._rtt_min

    @property
    def rtt_avg(self):
        return self._rtt_avg

    @property
    def rtt_max(self):
        return self._rtt_max

    @property
    def rtt_mdev(self):
        return self._rtt_mdev

    @property
    def packet_duplicate_rate(self):
        try:
            return (self.packet_duplicate_count / self.packet_receive) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def packet_duplicate_count(self):
        return self._duplicates

    def _find_ststs_head_line_idx(self, line_list, re_stats_header):
        for i, line in enumerate(line_list):
            if re_stats_header.search(line):
                break
        else:
            raise PingStaticticsHeaderNotFoundError(
                "ping statistics not found")

        return i

    def _validate_stats_body(self, body_line_list):
        if typepy.is_empty_sequence(body_line_list):
            raise EmptyPingStaticticsError("ping statistics is empty")

    def _initialize_parse_result(self):
        self._packet_transmit = None
        self._packet_receive = None
        self._rtt_min = None
        self._rtt_avg = None
        self._rtt_max = None
        self._rtt_mdev = None
        self._duplicates = None


class NullPingParser(PingParser):

    def parse(self, ping_message):  # pragma: no cover
        pass


class LinuxPingParser(PingParser):

    def parse(self, ping_message):
        logger.debug("parsing as Linux ping result format")

        self._initialize_parse_result()
        line_list = _to_unicode(ping_message).splitlines()

        i = self._find_ststs_head_line_idx(
            line_list, re.compile("--- .* ping statistics ---"))

        body_line_list = line_list[i + 1:]
        self._validate_stats_body(body_line_list)

        packet_line = body_line_list[0]
        packet_pattern = (
            pp.Word(pp.nums) +
            pp.Literal("packets transmitted,") +
            pp.Word(pp.nums) +
            pp.Literal("received,")
        )
        parse_list = packet_pattern.parseString(_to_unicode(packet_line))
        self._packet_transmit = int(parse_list[0])
        self._packet_receive = int(parse_list[2])

        self._duplicates = self.__parse_duplicate(packet_line)

        try:
            rtt_line = body_line_list[1]
        except IndexError:
            return
        if typepy.is_null_string(rtt_line):
            return

        rtt_pattern = (
            pp.Literal("rtt min/avg/max/mdev =") +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") + "/" +
            pp.Word(pp.nums + ".") +
            pp.Word(pp.nums + "ms")
        )
        try:
            parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))
        except pp.ParseException:
            return

        self._rtt_min = float(parse_list[1])
        self._rtt_avg = float(parse_list[3])
        self._rtt_max = float(parse_list[5])
        self._rtt_mdev = float(parse_list[7])

    @staticmethod
    def __parse_duplicate(line):
        packet_pattern = (
            pp.SkipTo(pp.Word("+" + pp.nums) + pp.Literal("duplicates,")) +
            pp.Word("+" + pp.nums) +
            pp.Literal("duplicates,")
        )
        try:
            duplicate_parse_list = packet_pattern.parseString(
                _to_unicode(line))
        except pp.ParseException:
            return 0

        return int(duplicate_parse_list[-2].strip("+"))


class WindowsPingParser(PingParser):

    def parse(self, ping_message):
        logger.debug("parsing as Windows ping result format")

        self._initialize_parse_result()
        line_list = _to_unicode(ping_message).splitlines()

        i = self._find_ststs_head_line_idx(
            line_list, re.compile("^Ping statistics for "))

        body_line_list = line_list[i + 1:]
        self._validate_stats_body(body_line_list)
        packet_line = body_line_list[0].strip()
        packet_pattern = (
            pp.Literal("Packets: Sent = ") +
            pp.Word(pp.nums) +
            pp.Literal(", Received = ") +
            pp.Word(pp.nums)
        )
        parse_list = packet_pattern.parseString(_to_unicode(packet_line))
        self._packet_transmit = int(parse_list[1])
        self._packet_receive = int(parse_list[3])

        try:
            rtt_line = body_line_list[2].strip()
        except IndexError:
            return
        if typepy.is_null_string(rtt_line):
            return
        rtt_pattern = (
            pp.Literal("Minimum = ") +
            pp.Word(pp.nums) +
            pp.Literal("ms, Maximum = ") +
            pp.Word(pp.nums) +
            pp.Literal("ms, Average = ") +
            pp.Word(pp.nums)
        )
        try:
            parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))
        except pp.ParseException:
            return

        self._rtt_min = float(parse_list[1])
        self._rtt_avg = float(parse_list[5])
        self._rtt_max = float(parse_list[3])
