# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import pytest
import six

from pingparsing import *


@pytest.fixture
def ping_text():
    return six.b("""
PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")

# ping google.com -q -c 60:
#   - Debian 8.2 w/ iputils-ping 20121221-5+b2
#   - Debian 5.0.10 w/ iputils-ping 20071127-1+lenny1
PING_DEBIAN = six.b("""PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")


# ping google.com -n 10:
#   Windows 7 SP1
PING_WINDOWS = six.b("""
Pinging google.com [216.58.196.238] with 32 bytes of data:
Reply from 216.58.196.238: bytes=32 time=87ms TTL=51
Reply from 216.58.196.238: bytes=32 time=97ms TTL=51
Reply from 216.58.196.238: bytes=32 time=56ms TTL=51
Reply from 216.58.196.238: bytes=32 time=95ms TTL=51
Reply from 216.58.196.238: bytes=32 time=194ms TTL=51
Reply from 216.58.196.238: bytes=32 time=98ms TTL=51
Reply from 216.58.196.238: bytes=32 time=93ms TTL=51
Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
Reply from 216.58.196.238: bytes=32 time=165ms TTL=51

Ping statistics for 216.58.196.238:
    Packets: Sent = 10, Received = 10, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 56ms, Maximum = 194ms, Average = 107ms
""")


@pytest.fixture
def ping_parser():
    return PingParsing()


class Test_PingParsing_parse:

    @pytest.mark.parametrize(["ping_text", "expected"], [
        [
            PING_DEBIAN,
            {
                "packet_transmit": 60,
                "packet_receive": 60,
                "packet_loss": 0.0,
                "rtt_min": 61.425,
                "rtt_avg": 99.731,
                "rtt_max": 212.597,
                "rtt_mdev": 27.566,
            }
        ],
        [
            PING_WINDOWS,
            {
                "packet_transmit": 10,
                "packet_receive": 10,
                "packet_loss": 0.0,
                "rtt_min": 56,
                "rtt_avg": 107,
                "rtt_max": 194,
                "rtt_mdev": None,
            }
        ]
    ])
    def test_normal(self, ping_parser, ping_text, expected):
        ping_parser.parse(ping_text)

        assert ping_parser.as_dict() == expected

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


class Test_PingTransmitter_ping:

    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["", 1, ValueError],
        ["test", 0, ValueError],
        ["test", -1, ValueError],
    ])
    def test_except(self, host, waittime, expected):
        transmitter = PingTransmitter()
        transmitter.destination_host = host
        transmitter.waittime = waittime
        with pytest.raises(expected):
            transmitter.ping()
