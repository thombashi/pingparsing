# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from pingparsing import PingTransmitter
import pytest
from typepy.type import RealNumber

from .common import ping_parser


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingTransmitter_ping(object):

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "waittime"], [
        ["localhost", 1],
        ["127.0.0.1", 1],
        ["::1", 1],
    ])
    def test_normal_waittime(self, transmitter, host, waittime):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "count", "waittime"], [
        ["localhost", 1, None],
        ["localhost", 1, 1000],
    ])
    def test_normal_count(self, transmitter, host, count, waittime):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        transmitter.count = count
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "count"], [
        ["localhost", 3],
    ])
    def test_normal_send_parse(
            self, transmitter, ping_parser, host, count):
        transmitter.destination_host = host
        transmitter.count = count
        result = transmitter.ping()

        ping_parser.parse(result.stdout)

        assert ping_parser.packet_transmit >= count
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss_rate).is_type()
        assert RealNumber(ping_parser.packet_loss_count).is_type()
        assert RealNumber(ping_parser.packet_duplicate_rate).is_type()
        assert RealNumber(ping_parser.packet_duplicate_count).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()

    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["", 1, ValueError],
        ["localhost", 0, ValueError],
        ["localhost", -1, ValueError],
        ["localhost", "a", ValueError],
        [None, 1, ValueError],
    ])
    def test_except_waittime(self,  transmitter, host, waittime, expected):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        with pytest.raises(expected):
            transmitter.ping()

    @pytest.mark.parametrize(["host", "count", "expected"], [
        ["localhost", 0, ValueError],
        ["localhost", -1, ValueError],
        ["localhost", "a", ValueError],
    ])
    def test_except_count(self,  transmitter, host, count, expected):
        transmitter.destination_host = host
        transmitter.count = count
        with pytest.raises(expected):
            transmitter.ping()
