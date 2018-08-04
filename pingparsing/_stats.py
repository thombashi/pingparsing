# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division, unicode_literals


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

        self.__icmp_reply_list = kwargs.pop("icmp_reply_list", [])

    @property
    def destination(self):
        """
        :return: The ping destination.
        :rtype: str
        """

        return self.__destination

    @property
    def packet_transmit(self):
        """
        :return: Number of packets transmitted.
        :rtype: int
        """

        return self.__packet_transmit

    @property
    def packet_receive(self):
        """
        :return: Number of packets received.
        :rtype: int
        """

        return self.__packet_receive

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
    def packet_loss_rate(self):
        """
        :return:
            Percentage of packet loss ``[%]``.
            ``None`` if the value is not a number.
        :rtype: float
        """

        try:
            return (self.packet_loss_count / self.packet_transmit) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def rtt_min(self):
        """
        :return:
            Minimum round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__rtt_min

    @property
    def rtt_avg(self):
        """
        :return:
            Average round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__rtt_avg

    @property
    def rtt_max(self):
        """
        :return:
            Maximum round trip time of transmitted ICMP packets ``[msec]``.
        :rtype: float
        """

        return self.__rtt_max

    @property
    def rtt_mdev(self):
        """
        :return:
            Standard deviation of transmitted ICMP packets. The attribute returns
            always ``None`` when parsing Windows ping result.
        :rtype: float
        """

        return self.__rtt_mdev

    @property
    def packet_duplicate_count(self):
        """
        :return:
            Number of duplicated packet. The attribute returns always ``None`` when parsing
            Windows ping result.
        :rtype: int
        """

        return self.__duplicates

    @property
    def packet_duplicate_rate(self):
        """
        :return:
            Percentage of duplicated packets ``[%]``. ``None`` if the value is not a number.
        :rtype: float
        """

        try:
            return (self.packet_duplicate_count / self.packet_receive) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def icmp_reply_list(self):
        """
        :return: List of ICMP packet reply information.
        :rtype: list of dict
        """

        return self.__icmp_reply_list

    def as_dict(self):
        """
        :return: ping statistics.
        :rtype: dict
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
        :return: ping statistics.
        :rtype: collections.namedtuple
        """

        from collections import namedtuple

        ping_result = self.as_dict()

        return namedtuple("PingStatsTuple", ping_result.keys())(**ping_result)
