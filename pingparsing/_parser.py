"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
import re
from datetime import datetime, tzinfo
from typing import Dict, List, Optional, Pattern, Sequence, Tuple, Union  # noqa

import pyparsing as pp
import typepy
from typepy import DateTime

from ._common import _to_unicode
from ._interface import PingParserInterface
from ._logger import logger
from ._stats import PingStats
from ._typing import IcmpReplies
from .error import ParseError, ParseErrorReason


class IcmpReplyKey:
    DESTINATION = "destination"
    BYTES = "bytes"
    TIMESTAMP = "timestamp"
    TIMESTAMP_NO_ANS = "timestamp_no_ans"
    SEQUENCE_NO = "icmp_seq"
    TTL = "ttl"
    TIME = "time"
    DUPLICATE = "duplicate"


class PingParser(PingParserInterface):
    _BYTES_PATTERN = rf"\s*(?P<{IcmpReplyKey.BYTES}>[0-9]+) bytes"
    _DEST_PATTERN = r"(?P<{key}>[a-zA-Z0-9:\-\.\(\)% ]+)".format(
        key=IcmpReplyKey.DESTINATION
    )  # host or ipv4/ipv6 addr
    _IPADDR_PATTERN = r"(\d{1,3}\.){3}\d{1,3}"
    _ICMP_SEQ_PATTERN = rf"\s*icmp_seq=(?P<{IcmpReplyKey.SEQUENCE_NO}>\d+)"
    _TTL_PATTERN = rf"\s*ttl=(?P<{IcmpReplyKey.TTL}>\d+)"
    _TIME_PATTERN = rf"\s*time[=<](?P<{IcmpReplyKey.TIME}>[0-9\.]+)"

    def __init__(self, timezone: Optional[tzinfo] = None) -> None:
        self.__timezone = timezone

    @abc.abstractproperty
    def _parser_name(self) -> str:  # pragma: no cover
        pass

    @abc.abstractproperty
    def _icmp_reply_pattern(self) -> str:  # pragma: no cover
        pass

    @property
    def _icmp_no_ans_pattern(self) -> str:
        return "(?!x)x"  # never matching anything

    @property
    def _duplicate_packet_pattern(self) -> str:
        return r".+ \(DUP!\)$"

    @abc.abstractproperty
    def _stats_headline_pattern(self) -> str:  # pragma: no cover
        pass

    @abc.abstractproperty
    def _is_support_packet_duplicate(self) -> bool:  # pragma: no cover
        pass

    def _parse_icmp_reply(self, ping_lines: Sequence[str]) -> IcmpReplies:
        icmp_reply_regexp = re.compile(self._icmp_reply_pattern, re.IGNORECASE)
        icmp_no_ans_regexp = re.compile(self._icmp_no_ans_pattern, re.IGNORECASE)
        duplicate_packet_regexp = re.compile(self._duplicate_packet_pattern)
        icmp_reply_list = []

        for line in ping_lines:
            match = icmp_reply_regexp.search(line)
            if not match:
                match = icmp_no_ans_regexp.search(line)
            if not match:
                continue

            results = match.groupdict()
            reply: Dict[str, Union[str, bool, float, int, datetime]] = {}

            if IcmpReplyKey.DESTINATION in results:
                reply[IcmpReplyKey.DESTINATION] = results[IcmpReplyKey.DESTINATION]

            if IcmpReplyKey.BYTES in results:
                reply[IcmpReplyKey.BYTES] = int(results[IcmpReplyKey.BYTES])

            if results.get(IcmpReplyKey.TIMESTAMP):
                reply[IcmpReplyKey.TIMESTAMP] = self.__timestamp_to_datetime(
                    results[IcmpReplyKey.TIMESTAMP]
                )
            elif results.get(IcmpReplyKey.TIMESTAMP_NO_ANS):
                reply[IcmpReplyKey.TIMESTAMP] = self.__timestamp_to_datetime(
                    results[IcmpReplyKey.TIMESTAMP_NO_ANS]
                )

            if IcmpReplyKey.SEQUENCE_NO in results:
                reply[IcmpReplyKey.SEQUENCE_NO] = int(results[IcmpReplyKey.SEQUENCE_NO])

            if IcmpReplyKey.TTL in results:
                reply[IcmpReplyKey.TTL] = int(results[IcmpReplyKey.TTL])

            if IcmpReplyKey.TIME in results:
                reply[IcmpReplyKey.TIME] = float(results[IcmpReplyKey.TIME])

            if duplicate_packet_regexp.search(line):
                reply[IcmpReplyKey.DUPLICATE] = True
            else:
                reply[IcmpReplyKey.DUPLICATE] = False

            icmp_reply_list.append(reply)

        return icmp_reply_list

    def _preprocess_parse_stats(self, lines: Sequence[str]) -> Tuple[str, str, Sequence[str]]:
        logger.debug(f"parsing as {self._parser_name:s} ping result format")

        stats_headline_idx = self.__find_stats_headline_idx(
            lines, re.compile(self._stats_headline_pattern)
        )
        body_line_list = lines[stats_headline_idx + 1 :]
        self.__validate_stats_body(body_line_list)

        packet_info_line = body_line_list[0]

        return (lines[stats_headline_idx], packet_info_line, body_line_list)

    def _parse_destination(self, stats_headline: str) -> str:
        match = re.search(self._stats_headline_pattern, stats_headline)
        if not match:
            return "unknown"

        return match.groupdict()[IcmpReplyKey.DESTINATION].strip(":")

    def __find_stats_headline_idx(self, lines: Sequence[str], re_stats_header: Pattern) -> int:
        for i, line in enumerate(lines):
            if re_stats_header.search(line):
                break
        else:
            raise ParseError(reason=ParseErrorReason.HEADER_NOT_FOUND)

        return i

    def __timestamp_to_datetime(self, timestamp: str) -> datetime:
        return DateTime(timestamp.lstrip("[").rstrip("]"), timezone=self.__timezone).force_convert()

    def __validate_stats_body(self, body_line_list: Sequence[str]) -> None:
        if typepy.is_empty_sequence(body_line_list):
            raise ParseError(reason=ParseErrorReason.EMPTY_STATISTICS)

    def _parse_duplicate(self, line: str) -> Optional[int]:
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
    def _parser_name(self) -> str:
        return "null"

    @property
    def _icmp_reply_pattern(self) -> str:
        return ""

    @property
    def _stats_headline_pattern(self) -> str:
        return ""

    @property
    def _is_support_packet_duplicate(self) -> bool:  # pragma: no cover
        return False

    def parse(self, ping_message: Sequence[str]) -> PingStats:  # pragma: no cover
        return PingStats()

    def _preprocess_parse_stats(
        self, lines: Sequence[str]
    ) -> Tuple[str, str, List[str]]:  # pragma: no cover
        return ("", "", [])


class LinuxPingParser(PingParser):
    @property
    def _parser_name(self) -> str:
        return "Linux"

    _TIMESTAMP_PATTERN = rf"(?P<{IcmpReplyKey.TIMESTAMP}>\[[0-9\.]+\])"
    _NO_ANS_TIMESTAMP_PATTERN = rf"(?P<{IcmpReplyKey.TIMESTAMP_NO_ANS}>\[[0-9\.]+\])"

    @property
    def _icmp_no_ans_pattern(self) -> str:
        return self._NO_ANS_TIMESTAMP_PATTERN + " no answer yet for " + self._ICMP_SEQ_PATTERN

    @property
    def _icmp_reply_pattern(self) -> str:
        return (
            self._TIMESTAMP_PATTERN
            + "?"
            + self._BYTES_PATTERN
            + r"\s+from "
            + self._DEST_PATTERN
            + ":"
            + self._ICMP_SEQ_PATTERN
            + self._TTL_PATTERN
            + self._TIME_PATTERN
        )

    @property
    def _stats_headline_pattern(self) -> str:
        return rf"--- {self._DEST_PATTERN} ping statistics ---"

    @property
    def _is_support_packet_duplicate(self) -> bool:
        return True

    def parse(self, ping_message: Sequence[str]) -> PingStats:
        icmp_replies = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            lines=ping_message
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
                icmp_replies=icmp_replies,
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
        try:
            parse_list = rtt_pattern.parseString(_to_unicode(rtt_line))
        except pp.ParseException:
            if not re.search(r"\s*pipe \d+", rtt_line):
                raise ValueError

            return PingStats(
                destination=destination,
                packet_transmit=packet_transmit,
                packet_receive=packet_receive,
                duplicates=duplicates,
                icmp_replies=icmp_replies,
            )

        return PingStats(
            destination=destination,
            packet_transmit=packet_transmit,
            packet_receive=packet_receive,
            duplicates=duplicates,
            rtt_min=float(parse_list[1]),
            rtt_avg=float(parse_list[3]),
            rtt_max=float(parse_list[5]),
            rtt_mdev=float(parse_list[7]),
            icmp_replies=icmp_replies,
        )


class WindowsPingParser(PingParser):
    @property
    def _parser_name(self) -> str:
        return "Windows"

    @property
    def _icmp_reply_pattern(self) -> str:
        return (
            " from "
            + self._DEST_PATTERN
            + rf":\s*bytes=(?P<{IcmpReplyKey.BYTES}>[0-9]+)"
            + self._TIME_PATTERN
            + "ms"
            + self._TTL_PATTERN
        )

    @property
    def _stats_headline_pattern(self) -> str:
        return rf"^Ping statistics for {self._DEST_PATTERN}"

    @property
    def _is_support_packet_duplicate(self) -> bool:
        return False

    def parse(self, ping_message: Sequence[str]) -> PingStats:
        icmp_replies = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            lines=ping_message
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
                icmp_replies=icmp_replies,
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
            icmp_replies=icmp_replies,
        )


class MacOsPingParser(PingParser):
    @property
    def _parser_name(self) -> str:
        return "macOS"

    @property
    def _icmp_reply_pattern(self) -> str:
        return (
            self._BYTES_PATTERN
            + r"\s+from "
            + self._DEST_PATTERN
            + ":"
            + self._ICMP_SEQ_PATTERN
            + self._TTL_PATTERN
            + self._TIME_PATTERN
        )

    @property
    def _stats_headline_pattern(self) -> str:
        return rf"--- {self._DEST_PATTERN} ping statistics ---"

    @property
    def _is_support_packet_duplicate(self) -> bool:
        return True

    def parse(self, ping_message: Sequence[str]) -> PingStats:
        icmp_replies = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            lines=ping_message
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
                icmp_replies=icmp_replies,
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
            icmp_replies=icmp_replies,
        )


class AlpineLinuxPingParser(LinuxPingParser):
    @property
    def _parser_name(self) -> str:
        return "AlpineLinux"

    @property
    def _icmp_reply_pattern(self) -> str:
        return (
            self._BYTES_PATTERN
            + r"\s+from "
            + self._DEST_PATTERN
            + ": "
            + rf"seq=(?P<{IcmpReplyKey.SEQUENCE_NO}>\d+) "
            + self._TTL_PATTERN
            + self._TIME_PATTERN
        )

    @property
    def _is_support_packet_duplicate(self) -> bool:
        return True

    def parse(self, ping_message: Sequence[str]) -> PingStats:
        icmp_replies = self._parse_icmp_reply(ping_message)
        stats_headline, packet_info_line, body_line_list = self._preprocess_parse_stats(
            lines=ping_message
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
                icmp_replies=icmp_replies,
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
            icmp_replies=icmp_replies,
        )

    def _parse_duplicate(self, line: str) -> int:
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
