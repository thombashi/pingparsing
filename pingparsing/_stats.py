"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from typing import Dict, Optional, Tuple, Union, cast

from ._typing import IcmpReplies


class PingStats:
    def __init__(self, *args, **kwargs) -> None:
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
    def destination(self) -> str:
        """
        The ping destination.

        Returns:
            |str|:
        """

        return self.__destination

    @property
    def packet_transmit(self) -> Optional[int]:
        """
        Number of packets transmitted.

        Returns:
            |int|:
        """

        return self.__packet_transmit

    @property
    def packet_receive(self) -> Optional[int]:
        """
        Number of packets received.

        Returns:
            |int|:
        """

        return self.__packet_receive

    @property
    def packet_loss_count(self) -> Optional[int]:
        """
        Number of packet losses.

        Returns:
            |int|: |None| if the value is not a number.
        """

        try:
            return cast(int, self.packet_transmit) - cast(int, self.packet_receive)
        except TypeError:
            return None

    @property
    def packet_loss_rate(self) -> Optional[float]:
        """
        Percentage of packet loss |percent_unit|.

        Returns:
            |float|: |None| if the value is not a number.
        """

        try:
            return (cast(int, self.packet_loss_count) / cast(int, self.packet_transmit)) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def rtt_min(self) -> Optional[float]:
        """
        Minimum round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_min

    @property
    def rtt_avg(self) -> Optional[float]:
        """
        Average round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_avg

    @property
    def rtt_max(self) -> Optional[float]:
        """
        Maximum round trip time of transmitted ICMP packets |msec_unit|.

        Returns:
            |float|:
        """

        return self.__rtt_max

    @property
    def rtt_mdev(self) -> Optional[float]:
        """
        Standard deviation of transmitted ICMP packets.

        Returns:
            |float|: |None| when parsing Windows ping result.
        """

        return self.__rtt_mdev

    @property
    def packet_duplicate_count(self) -> Optional[int]:
        """
        Number of duplicated packets.

        Returns:
            |int|: |None| when parsing Windows ping result.
        """

        return self.__duplicates

    @property
    def packet_duplicate_rate(self) -> Optional[float]:
        """
        Percentage of duplicated packets |percent_unit|.

        Returns:
            |float|: |None| if the value is not a number.
        """

        try:
            return (cast(int, self.packet_duplicate_count) / cast(int, self.packet_receive)) * 100
        except (TypeError, ZeroDivisionError, OverflowError):
            return None

    @property
    def icmp_replies(self) -> IcmpReplies:
        """
        ICMP packet reply information.

            .. note:
                ``time<1ms`` considered as ``time=1``

        Returns:
            |list| of |dict|:
        """

        return self.__icmp_replies

    def is_empty(self):
        return all(
            [
                self.destination is None,
                self.packet_transmit is None,
                self.packet_receive is None,
                self.packet_loss_count is None,
                self.packet_loss_rate is None,
                self.packet_duplicate_count is None,
                self.packet_duplicate_rate is None,
                self.rtt_min is None,
                self.rtt_avg is None,
                self.rtt_max is None,
                self.rtt_mdev is None,
                not self.icmp_replies,
            ]
        )

    def as_dict(
        self, include_icmp_replies: bool = False
    ) -> Dict[str, Union[str, int, float, IcmpReplies, None]]:
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

        d: Dict[str, Union[str, int, float, IcmpReplies, None]] = {
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
        if include_icmp_replies:
            d["icmp_replies"] = self.icmp_replies

        return d

    def as_tuple(self) -> Tuple:
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
        """  # noqa

        from collections import namedtuple

        ping_result = self.as_dict()

        return namedtuple("PingStatsTuple", ping_result.keys())(**ping_result)  # type: ignore
