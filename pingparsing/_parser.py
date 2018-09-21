# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division

import abc
import re
from datetime import datetime

import pyparsing as pp
import typepy
from typepy import Integer

from ._common import _to_unicode
from ._interface import PingParserInterface
from ._logger import logger
from ._stats import PingStats
from .error import ParseError, ParseErrorReason


class PingParser(PingParserInterface):

    _IPADDR_PATTERN = r"(\d{1,3}\.){3}\d{1,3}"
    _ICMP_SEQ_PATTERN = r"icmp_seq=(?P<icmp_seq>\d+)"
    _TTL_PATTERN = r"ttl=(?P<ttl>\d+)"
    _TIME_PATTERN = r"time=(?P<time>[0-9\.]+)"

    @abc.abstractproperty
    def _parser_name(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _icmp_reply_pattern(self):  # pragma: no cover
        pass

    @property
    def _duplicate_packet_pattern(self):
        return r".+ \(DUP!\)$"

    @abc.abstractproperty
    def _stats_headline_pattern(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _is_support_packet_duplicate(self):  # pragma: no cover
        pass

    def _parse_icmp_reply(self, ping_line_list):
        icmp_reply_regexp = re.compile(self._icmp_reply_pattern, re.IGNORECASE)
        duplicate_packet_regexp = re.compile(self._duplicate_packet_pattern)
        icmp_reply_list = []

        for line in ping_line_list:
            match = icmp_reply_regexp.search(line)
            if not match:
                continue

            reply = match.groupdict()

            if reply.get("timestamp"):
                reply["timestamp"] = datetime.fromtimestamp(
                    Integer(reply["timestamp"].lstrip("[").rstrip("]")).force_convert()
                )

            if reply.get("icmp_seq"):
                reply["icmp_seq"] = int(reply["icmp_seq"])

            if reply.get("ttl"):
                reply["ttl"] = int(reply["ttl"])

            if reply.get("time"):
                reply["time"] = float(reply["time"])

            if duplicate_packet_regexp.search(line):
                reply["duplicate"] = True
            else:
                reply["duplicate"] = False

            icmp_reply_list.append(reply)

        return icmp_reply_list

    def _preprocess_parse_stats(self, line_list):
        logger.debug("parsing as {:s} ping result format".format(self._parser_name))

        stats_headline_idx = self.__find_stats_headline_idx(
            line_list, re.compile(self._stats_headline_pattern)
        )
        body_line_list = line_list[stats_headline_idx + 1 :]
        self.__validate_stats_body(body_line_list)

        packet_info_line = body_line_list[0]

        return (line_list[stats_headline_idx], packet_info_line, body_line_list)

    def _parse_destination(self, stats_headline):
        return stats_headline.lstrip("--- ").rstrip(" ping statistics ---")

    def __find_stats_headline_idx(self, line_list, re_stats_header):
        for i, line in enumerate(line_list):
            if re_stats_header.search(line):
                break
        else:
            raise ParseError(reason=ParseErrorReason.HEADER_NOT_FOUND)

        return i

    def __validate_stats_body(self, body_line_list):
        if typepy.is_empty_sequence(body_line_list):
            raise ParseError(reason=ParseErrorReason.EMPTY_STATISTICS)

    def _parse_duplicate(self, line):
        if not self._is_support_packet_duplicate:
            return None

        packet_pattern = (
            pp.SkipTo(pp.Word("+" + pp.nums) + pp.Literal("duplicates,"))
            + pp.Word("+" + pp.nums)
            + pp.Literal("duplicates,")
        )

        try:
            duplicate_parse_list = packet_pattern.parseString(_to_unicode(line))
        except pp.ParseException:
            return 0

        return int(duplicate_parse_list[-2].strip("+"))


class NullPingParser(PingParser):
    @property
    def _parser_name(self):
        return "null"

    @property
    def _icmp_reply_pattern(self):
        return ""

    @property
    def _stats_headline_pattern(self):
        return ""

    @property
    def _is_support_packet_duplicate(self):  # pragma: no cover
        return False

    def parse(self, ping_message):  # pragma: no cover
        pass

    def _preprocess_parse_stats(self, line_list):  # pragma: no cover
        pass


class LinuxPingParser(PingParser):
    @property
    def _parser_name(self):
        return "Linux"

    @property
    def _icmp_reply_pattern(self):
        return (
            r"(?P<timestamp>\[[0-9\.]+\])?\s?.+ from "
            + self._IPADDR_PATTERN
            + ".*"
            + self._ICMP_SEQ_PATTERN
            + " "
            + self._TTL_PATTERN
            + " "
            + self._TIME_PATTERN
        )

    @property
    def _stats_headline_pattern(self):
        return "--- .* ping statistics ---"

    @property
    def _is_support_packet_duplicate(self):
        return True

    def parse(self, ping_message):
        icmp_reply_list = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            line_list=ping_message
        )
        packet_pattern = (
            pp.Word(pp.nums)
            + pp.Literal("packets transmitted,")
            + pp.Word(pp.nums)
            + pp.Literal("received,")
        )

        destination = self._parse_destination(stats_headline)
        duplicates = self._parse_duplicate(packet_info_line)

        parse_list = packet_pattern.parseString(_to_unicode(packet_info_line))
        packet_transmit = int(parse_list[0])
        packet_receive = int(parse_list[2])

        is_valid_data = True
        try:
            rtt_line = body_line_list[1]
        except IndexError:
            is_valid_data = False

        if not is_valid_data or typepy.is_null_string(rtt_line):
            return PingStats(
                destination=destination,
                packet_transmit=packet_transmit,
                packet_receive=packet_receive,
                duplicates=duplicates,
                icmp_reply_list=icmp_reply_list,
            )

        rtt_pattern = (
            pp.Literal("rtt min/avg/max/mdev =")
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + pp.Word(pp.nums + "ms")
        )
        parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))

        return PingStats(
            destination=destination,
            packet_transmit=packet_transmit,
            packet_receive=packet_receive,
            duplicates=duplicates,
            rtt_min=float(parse_list[1]),
            rtt_avg=float(parse_list[3]),
            rtt_max=float(parse_list[5]),
            rtt_mdev=float(parse_list[7]),
            icmp_reply_list=icmp_reply_list,
        )


class WindowsPingParser(PingParser):
    @property
    def _parser_name(self):
        return "Windows"

    @property
    def _icmp_reply_pattern(self):
        return " from " + self._IPADDR_PATTERN + ".*" + self._TTL_PATTERN + " " + self._TIME_PATTERN

    @property
    def _stats_headline_pattern(self):
        return "^Ping statistics for "

    @property
    def _is_support_packet_duplicate(self):
        return False

    def parse(self, ping_message):
        icmp_reply_list = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            line_list=ping_message
        )
        packet_pattern = (
            pp.Literal("Packets: Sent = ")
            + pp.Word(pp.nums)
            + pp.Literal(", Received = ")
            + pp.Word(pp.nums)
        )

        destination = self._parse_destination(stats_headline)
        duplicates = self._parse_duplicate(packet_info_line)

        parse_list = packet_pattern.parseString(_to_unicode(packet_info_line))
        packet_transmit = int(parse_list[1])
        packet_receive = int(parse_list[3])

        is_valid_data = True
        try:
            rtt_line = body_line_list[2].strip()
        except IndexError:
            is_valid_data = False

        if not is_valid_data or typepy.is_null_string(rtt_line):
            return PingStats(
                destination=destination,
                packet_transmit=packet_transmit,
                packet_receive=packet_receive,
                duplicates=duplicates,
                icmp_reply_list=icmp_reply_list,
            )

        rtt_pattern = (
            pp.Literal("Minimum = ")
            + pp.Word(pp.nums)
            + pp.Literal("ms, Maximum = ")
            + pp.Word(pp.nums)
            + pp.Literal("ms, Average = ")
            + pp.Word(pp.nums)
        )
        parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))

        return PingStats(
            destination=destination,
            packet_transmit=packet_transmit,
            packet_receive=packet_receive,
            duplicates=duplicates,
            rtt_min=float(parse_list[1]),
            rtt_avg=float(parse_list[5]),
            rtt_max=float(parse_list[3]),
            icmp_reply_list=icmp_reply_list,
        )

    def _parse_destination(self, stats_headline):
        return stats_headline.lstrip("Ping statistics for ").rstrip(":")


class MacOsPingParser(PingParser):
    @property
    def _parser_name(self):
        return "macOS"

    @property
    def _icmp_reply_pattern(self):
        return (
            " from "
            + self._IPADDR_PATTERN
            + ".*"
            + self._ICMP_SEQ_PATTERN
            + " "
            + self._TTL_PATTERN
            + " "
            + self._TIME_PATTERN
        )

    @property
    def _stats_headline_pattern(self):
        return "--- .* ping statistics ---"

    @property
    def _is_support_packet_duplicate(self):
        return True

    def parse(self, ping_message):
        icmp_reply_list = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            line_list=ping_message
        )
        packet_pattern = (
            pp.Word(pp.nums)
            + pp.Literal("packets transmitted,")
            + pp.Word(pp.nums)
            + pp.Literal("packets received,")
        )

        destination = self._parse_destination(stats_headline)
        duplicates = self._parse_duplicate(packet_info_line)

        parse_list = packet_pattern.parseString(_to_unicode(packet_info_line))
        packet_transmit = int(parse_list[0])
        packet_receive = int(parse_list[2])

        is_valid_data = True
        try:
            rtt_line = body_line_list[1]
        except IndexError:
            is_valid_data = False

        if not is_valid_data or typepy.is_null_string(rtt_line):
            return PingStats(
                destination=destination,
                packet_transmit=packet_transmit,
                packet_receive=packet_receive,
                duplicates=duplicates,
                icmp_reply_list=icmp_reply_list,
            )

        rtt_pattern = (
            pp.Literal("round-trip min/avg/max/stddev =")
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + pp.Word(pp.nums + "ms")
        )
        parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))

        return PingStats(
            destination=destination,
            packet_transmit=packet_transmit,
            packet_receive=packet_receive,
            duplicates=duplicates,
            rtt_min=float(parse_list[1]),
            rtt_avg=float(parse_list[3]),
            rtt_max=float(parse_list[5]),
            rtt_mdev=float(parse_list[7]),
            icmp_reply_list=icmp_reply_list,
        )


class AlpineLinuxPingParser(LinuxPingParser):
    @property
    def _parser_name(self):
        return "AlpineLinux"

    @property
    def _icmp_reply_pattern(self):
        return (
            " from "
            + self._IPADDR_PATTERN
            + ".*"
            + r"seq=(?P<icmp_seq>\d+) "
            + self._TTL_PATTERN
            + " "
            + self._TIME_PATTERN
        )

    @property
    def _is_support_packet_duplicate(self):
        return True

    def parse(self, ping_message):
        icmp_reply_list = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            line_list=ping_message
        )
        packet_pattern = (
            pp.Word(pp.nums)
            + pp.Literal("packets transmitted,")
            + pp.Word(pp.nums)
            + pp.Literal("packets received,")
        )

        destination = self._parse_destination(stats_headline)
        duplicates = self._parse_duplicate(packet_info_line)

        parse_list = packet_pattern.parseString(_to_unicode(packet_info_line))
        packet_transmit = int(parse_list[0])
        packet_receive = int(parse_list[2])

        is_valid_data = True
        try:
            rtt_line = body_line_list[1]
        except IndexError:
            is_valid_data = False

        if not is_valid_data or typepy.is_null_string(rtt_line):
            return PingStats(
                destination=destination,
                packet_transmit=packet_transmit,
                packet_receive=packet_receive,
                duplicates=duplicates,
                icmp_reply_list=icmp_reply_list,
            )

        rtt_pattern = (
            pp.Literal("round-trip min/avg/max =")
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + "/"
            + pp.Word(pp.nums + ".")
            + pp.Word(pp.nums + "ms")
        )
        parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))

        return PingStats(
            destination=destination,
            packet_transmit=packet_transmit,
            packet_receive=packet_receive,
            duplicates=duplicates,
            rtt_min=float(parse_list[1]),
            rtt_avg=float(parse_list[3]),
            rtt_max=float(parse_list[5]),
            icmp_reply_list=icmp_reply_list,
        )

    def _parse_duplicate(self, line):
        packet_pattern = (
            pp.SkipTo(pp.Word(pp.nums) + pp.Literal("duplicates,"))
            + pp.Word(pp.nums)
            + pp.Literal("duplicates,")
        )
        try:
            duplicate_parse_list = packet_pattern.parseString(_to_unicode(line))
        except pp.ParseException:
            return 0

        return int(duplicate_parse_list[-2])
