# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals

import warnings


class PingStats(object):
    def __init__(self, *args, **kwargs):
        self.__destination = kwargs.pop("destination", None)
        self.__packet_transmit = kwargs.pop("packet_transmit", None)
        self.__packet_receive = kwargs.pop("packet_receive", None)
        self.__rtt_min = kwargs.pop("rtt_min", None)
        self.__rtt_avg = kwargs.pop("rtt_avg", None)
        self.__rtt_max = kwargs.pop("rtt_max", None)
        self.__rtt_mdev = kwargs.pop("rtt_mdev", None)
        self.__duplicates = kwargs.pop("duplicates", None)

        self.__icmp_replies = kwargs.pop("icmp_replies", [])

    @property
    def destination(self):
        """
        The ping destination.

        Returns:
            |str|:
        """

        return self.__destination

    @property
    def packet_transmit(self):
        """
        Number of packets transmitted.

        Returns:
            |int|:
        """

        return self.__packet_transmit

    @property
    def packet_receive(self):
        """
        Number of packets received.

        Returns:
            |int|:
        """

        return self.__packet_receive

    @property
    def packet_loss_count(self):
        """
        Number of packet losses.

        Returns:
            |int|: |None| if the value is not a number.
        """

        try:
            return self.packet_transmit - self.packet_receive
        except TypeError:
            return None

    @property
    def packet_loss_rate(self):
        """
        Percentage of packet loss |percent_unit|.

        Returns:
            |float|: |None| if the value is not a number.
        """

        try:
            return (self.packet_loss_count / self.packet_transmit) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def rtt_min(self):
        """
        Minimum round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_min

    @property
    def rtt_avg(self):
        """
        Average round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_avg

    @property
    def rtt_max(self):
        """
        Maximum round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_max

    @property
    def rtt_mdev(self):
        """
        Standard deviation of transmitted ICMP packets.

        Returns:
            |float|: |None| when parsing Windows ping result.
        """

        return self.__rtt_mdev

    @property
    def packet_duplicate_count(self):
        """
        Number of duplicated packets.

        Returns:
            |int|: |None| when parsing Windows ping result.
        """

        return self.__duplicates

    @property
    def packet_duplicate_rate(self):
        """
        Percentage of duplicated packets |percent_unit|.

        Returns:
            |float|: |None| if the value is not a number.
        """

        try:
            return (self.packet_duplicate_count / self.packet_receive) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def icmp_replies(self):
        """
        ICMP packet reply information.

        Returns:
            |list| of |dict|:
        """

        return self.__icmp_replies

    @property
    def icmp_reply_list(self):
        warnings.warn("'icmp_reply_list' has moved to 'icmp_replies'", DeprecationWarning)

        return self.icmp_replies

    def as_dict(self):
        """
        ping statistics.

        Returns:
            |dict|:

        Examples:
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

        return {
            "destination": self.destination,
            "packet_transmit": self.packet_transmit,
            "packet_receive": self.packet_receive,
            "packet_loss_count": self.packet_loss_count,
            "packet_loss_rate": self.packet_loss_rate,
            "rtt_min": self.rtt_min,
            "rtt_avg": self.rtt_avg,
            "rtt_max": self.rtt_max,
            "rtt_mdev": self.rtt_mdev,
            "packet_duplicate_count": self.packet_duplicate_count,
            "packet_duplicate_rate": self.packet_duplicate_rate,
        }

    def as_tuple(self):
        """
        ping statistics.

        Returns:
            |namedtuple|:

        Examples:
            >>> import pingparsing
            >>> parser = pingparsing.PingParsing()
            >>> parser.parse(ping_result)
            >>> parser.as_tuple()
            PingResult(destination='google.com', packet_transmit=60, packet_receive=60, packet_loss_rate=0.0, packet_loss_count=0, rtt_min=61.425, rtt_avg=99.731, rtt_max=212.597, rtt_mdev=27.566, packet_duplicate_rate=0.0, packet_duplicate_count=0)
        """

        from collections import namedtuple

        ping_result = self.as_dict()

        return namedtuple("PingStatsTuple", ping_result.keys())(**ping_result)
