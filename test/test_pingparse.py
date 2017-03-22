# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from pingparsing import (
    PingParsing,
    PingTransmitter,
)
import pytest
from typepy.type import RealNumber


@pytest.fixture
def ping_parser():
    return PingParsing()


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingParse_parse:

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "value", "expected"], [
        ["localhost", None, 1],
        ["localhost", 3, 3],
        ["127.0.0.1", 1, 1],
        ["::1", 1, 1],
    ])
    def test_normal(
            self, transmitter, ping_parser, host, value, expected):
        transmitter.destination_host = host
        transmitter.count = value
        transmitter.waittime = value
        result = transmitter.ping()

        ping_parser.parse(result.stdout)

        assert ping_parser.packet_transmit >= expected
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["localhost", 1, 1],
        ["localhost", 3, 3],
    ])
    def test_normal_waittime(
            self, transmitter, ping_parser, host, waittime, expected):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        result = transmitter.ping()

        ping_parser.parse(result.stdout)

        assert ping_parser.packet_transmit >= expected
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "count", "expected"], [
        ["localhost", 1, 1],
        ["localhost", 3, 3],
    ])
    def test_normal_count(
            self, transmitter, ping_parser, host, count, expected):
        transmitter.destination_host = host
        transmitter.count = count
        result = transmitter.ping()

        ping_parser.parse(result.stdout)

        assert ping_parser.packet_transmit == expected
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()
