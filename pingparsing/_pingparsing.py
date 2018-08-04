# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division

import pyparsing as pp
import typepy

from ._common import _to_unicode
from ._interface import PingParserInterface
from ._logger import logger
from ._parser import (
    AlpineLinuxPingParser,
    LinuxPingParser,
    MacOsPingParser,
    NullPingParser,
    WindowsPingParser,
)
from ._stats import PingStats
from .error import ParseError, ParseErrorReason


class PingParsing(PingParserInterface):
    """
    Parser class to parsing ping command output.
    """

    def __init__(self):
        self.__parser = NullPingParser()
        self.__stats = None

    @property
    def parser_name(self):
        return self.__parser._parser_name

    @property
    def destination(self):
        """
        (Duprecated)

        :return: The ping destination.
        :rtype: str
        """

        return self.__stats.destination

    @property
    def packet_transmit(self):
        """
        (Duprecated)

        :return: Number of packets transmitted.
        :rtype: int
        """

        return self.__stats.packet_transmit

    @property
    def packet_receive(self):
        """
        (Duprecated)

        :return: Number of packets received.
        :rtype: int
        """

        return self.__stats.packet_receive

    @property
    def packet_loss_rate(self):
        """
        (Duprecated)

        :return:
            Percentage of packet loss ``[%]``.
            ``None`` if the value is not a number.
        :rtype: float
        """

        return self.__stats.packet_loss_rate

    @property
    def packet_loss(self):
        # mark as delete
        return self.packet_loss_rate

    @property
    def packet_loss_count(self):
        """
        (Duprecated)

        :return: Packet loss count. ``None`` if the value is not a number.
        :rtype: int
        """

        return self.__stats.packet_loss_count

    @property
    def rtt_min(self):
        """
        (Duprecated)

        :return:
            Minimum round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__stats.rtt_min

    @property
    def rtt_avg(self):
        """
        (Duprecated)

        :return:
            Average round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__stats.rtt_avg

    @property
    def rtt_max(self):
        """
        (Duprecated)

        :return:
            Maximum round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__stats.rtt_max

    @property
    def rtt_mdev(self):
        """
        (Duprecated)

        :return:
            Standard deviation of transmitted ICMP packets. The attribute
            returns always ``None`` when parsing Windows ping result.
        :rtype: float
        """

        return self.__stats.rtt_mdev

    @property
    def packet_duplicate_rate(self):
        """
        (Duprecated)

        :return:
            Percentage of duplicated packets ``[%]``.
            ``None`` if the value is not a number.
        :rtype: float
        """

        return self.__stats.packet_duplicate_rate

    @property
    def packet_duplicate_count(self):
        """
        (Duprecated)

        :return:
            Number of duplicated packet. The attribute
            returns always ``None`` when parsing Windows ping result.
        :rtype: int
        """

        return self.__stats.packet_duplicate_count

    @property
    def duplicates(self):
        # mark as delete
        return self.packet_duplicate_count

    def as_dict(self):
        """
        (Duprecated)

        :return: Parsed result as a dictionary.
        :rtype: dict

        :Examples:
            >>> import pingparsing
            >>> parser = pingparsing.PingParsing()
            >>> parser.parse(ping_result)
            >>> parser.as_dict()
            {
                "destination": "google.com",
                "packet_transmit": 60,
                "packet_receive": 60,
                "packet_loss_rate": 0.0,
                "packet_loss_count": 0,
                "rtt_min": 61.425,
                "rtt_avg": 99.731,
                "rtt_max": 212.597,
                "rtt_mdev": 27.566,
                "packet_duplicate_rate": 0.0,
                "packet_duplicate_count": 0
            }
        """

        return self.__stats.as_dict()

    def as_tuple(self):
        """
        (Duprecated)

        :return: Parsed result as a tuple.
        :rtype: collections.namedtuple

        :Examples:
            >>> import pingparsing
            >>> parser = pingparsing.PingParsing()
            >>> parser.parse(ping_result)
            >>> parser.as_tuple()
            PingResult(destination='google.com', packet_transmit=60, packet_receive=60, packet_loss_rate=0.0, packet_loss_count=0, rtt_min=61.425, rtt_avg=99.731, rtt_max=212.597, rtt_mdev=27.566, packet_duplicate_rate=0.0, packet_duplicate_count=0)
        """

        return self.__stats.as_tuple()

    def parse(self, ping_message):
        """
        Parse ping command output.

        :param ping_message: ping command output.
        :type ping_message: str or :py:class:`~pingparsing.PingResult`
        :return: Parsed result.

            .. seealso:: :py:meth:`.as_tuple`
        :rtype: :py:class:`~pingparsing.PingStats`
        """

        try:
            # accept PingResult instance as an input
            if typepy.is_not_null_string(ping_message.stdout):
                ping_message = ping_message.stdout
        except AttributeError:
            pass

        logger.debug("parsing ping result: {}".format(ping_message))

        self.__parser = NullPingParser()

        if typepy.is_null_string(ping_message):
            logger.debug("ping_message is empty")
            self.__stats = PingStats()

            return self.__stats

        line_list = _to_unicode(ping_message).splitlines()
        parser_class_list = (
            LinuxPingParser,
            WindowsPingParser,
            MacOsPingParser,
            AlpineLinuxPingParser,
        )

        for parser_class in parser_class_list:
            self.__parser = parser_class()
            try:
                self.__stats = self.__parser.parse(line_list)
                return self.__stats
            except ParseError as e:
                if e.reason != ParseErrorReason.HEADER_NOT_FOUND:
                    raise e
            except pp.ParseException:
                pass

        self.__parser = NullPingParser()

        return self.__stats
