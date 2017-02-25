# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from pingparsing import *
import pytest
from typepy.type import RealNumber


class Test_PingParse_parse:

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["localhost", 3, ValueError],
    ])
    def test_normal(self, host, waittime, expected):
        transmitter = PingTransmitter()
        transmitter.destination_host = host
        transmitter.waittime = waittime
        result = transmitter.ping()

        ping_parser = PingParsing()
        ping_parser.parse(result.stdout)

        assert RealNumber(ping_parser.packet_transmit).is_type()
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()
