# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import division

import typepy

import pyparsing as pp

from ._common import _to_unicode
from ._interface import PingParserInterface
from ._logger import logger
from ._parser import (
    NullPingParser,
    LinuxPingParser,
    WindowsPingParser,
    OsxPingParser,
)
from .error import PingStatisticsHeaderNotFoundError


class PingParsing(PingParserInterface):
    """
    Parser class to parsing ping command output.
    """

    def __init__(self):
        self.ping_option = ""

        self.__parser = NullPingParser()

    @property
    def packet_transmit(self):
        """
        :return: Number of packets transmitted.
        :rtype: int
        """

        return self.__parser.packet_transmit

    @property
    def packet_receive(self):
        """
        :return: Number of packets received.
        :rtype: int
        """

        return self.__parser.packet_receive

    @property
    def packet_loss_rate(self):
        """
        :return:
            Percentage of packet loss [%].
            ``None`` if the value is not a number.
        :rtype: float
        """

        try:
            return (1.0 - (self.packet_receive / self.packet_transmit)) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def packet_loss(self):
        # mark as delete
        return self.packet_loss_rate

    @property
    def packet_loss_count(self):
        """
        :return: Packet loss count. ``None`` if the value is not a number.
        :rtype: int
        """

        try:
            return self.packet_transmit - self.packet_receive
        except TypeError:
            return None

    @property
    def rtt_min(self):
        """
        :return: Minimum round trip time of transmitted ICMP packets [ms].
        :rtype: float
        """

        return self.__parser.rtt_min

    @property
    def rtt_avg(self):
        """
        :return: Average round trip time of transmitted ICMP packets [ms].
        :rtype: float
        """

        return self.__parser.rtt_avg

    @property
    def rtt_max(self):
        """
        :return: Maximum round trip time of transmitted ICMP packets [ms].
        :rtype: float
        """

        return self.__parser.rtt_max

    @property
    def rtt_mdev(self):
        """
        :return: Standard deviation of transmitted ICMP packets (Linux only).
        :rtype: float
        """

        return self.__parser.rtt_mdev

    @property
    def packet_duplicate_rate(self):
        """
        :return:
            Percentage of duplicated packets [%].
            ``None`` if the value is not a number.
        :rtype: float
        """

        try:
            return (self.packet_duplicate_count / self.packet_receive) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def packet_duplicate_count(self):
        """
        :return: Number of duplicated packet (Linux only).
        :rtype: int
        """

        return self.__parser.packet_duplicate_count

    @property
    def duplicates(self):
        # mark as delete
        return self.packet_duplicate_count

    def as_dict(self):
        """
        :return: Parsed result as a dictionary.
        :rtype: dict
        """

        return {
            "packet_transmit": self.packet_transmit,
            "packet_receive": self.packet_receive,
            "packet_loss_rate": self.packet_loss_rate,
            "packet_loss_count": self.packet_loss_count,
            "rtt_min": self.rtt_min,
            "rtt_avg": self.rtt_avg,
            "rtt_max": self.rtt_max,
            "rtt_mdev": self.rtt_mdev,
            "packet_duplicate_rate": self.packet_duplicate_rate,
            "packet_duplicate_count": self.packet_duplicate_count,
        }

    def parse(self, ping_message):
        """
        Parse ping command output.
        You can get parsing results by following attributes:

            - :py:attr:`.packet_transmit`
            - :py:attr:`.packet_receive`
            - :py:attr:`.packet_loss_rate`
            - :py:attr:`.packet_loss_count`
            - :py:attr:`.packet_duplicate_rate`
            - :py:attr:`.packet_duplicate_count`
            - :py:attr:`.rtt_min`
            - :py:attr:`.rtt_avg`
            - :py:attr:`.rtt_max`
            - :py:attr:`.rtt_mdev`

        Alternatively, you can get data as a dictionary by :py:meth:`.as_dict`

        :param ping_message: ping command output.
        :type ping_message: str or pingparsing.PingResult
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
            return

        line_list = _to_unicode(ping_message).splitlines()

        self.__parser = LinuxPingParser()
        try:
            self.__parser.parse(line_list)
            return
        except (PingStatisticsHeaderNotFoundError, pp.ParseException):
            pass

        self.__parser = WindowsPingParser()
        try:
            self.__parser.parse(line_list)
            return
        except (PingStatisticsHeaderNotFoundError, pp.ParseException):
            pass

        self.__parser = OsxPingParser()
        try:
            self.__parser.parse(line_list)
            return
        except (PingStatisticsHeaderNotFoundError, pp.ParseException):
            pass

        self.__parser = NullPingParser()
