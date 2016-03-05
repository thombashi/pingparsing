# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import pytest
from pingparsing import *


@pytest.fixture
def ping_text():
    return """
PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
"""


@pytest.fixture
def ping_parser():
    return PingParsing()


class Test_PingParsing_parse:

    def test_normal(self, ping_parser, ping_text):
        ping_parser.parse(ping_text)

        assert ping_parser.packet_transmit == 60
        assert ping_parser.packet_receive == 60
        assert ping_parser.packet_loss == 0
        assert ping_parser.rtt_min == 61.425
        assert ping_parser.rtt_avg == 99.731
        assert ping_parser.rtt_max == 212.597
        assert ping_parser.rtt_mdev == 27.566

    def test_empty(self, ping_parser, ping_text):
        ping_parser.parse(ping_text)
        ping_parser.parse("")

        assert ping_parser.packet_transmit is None
        assert ping_parser.packet_receive is None
        assert ping_parser.packet_loss is None
        assert ping_parser.rtt_min is None
        assert ping_parser.rtt_avg is None
        assert ping_parser.rtt_max is None
        assert ping_parser.rtt_mdev is None


class Test_PingParsing_ping:

    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["", 1, ValueError],
        ["test", 0, ValueError],
        ["test", -1, ValueError],
    ])
    def test_except(self, ping_parser, host, waittime, expected):
        ping_parser.destination_host = host
        ping_parser.waittime = waittime
        with pytest.raises(expected):
            ping_parser.ping()
