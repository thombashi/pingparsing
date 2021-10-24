"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from datetime import datetime
from textwrap import dedent

import pytest
import pytz

from pingparsing import ParseError, PingResult

from .common import PingTestData, ping_parser  # noqa: W0611
from .data import (
    DEBIAN_SUCCESS_0,
    UBUNTU_SUCCESS_0,
    UBUNTU_SUCCESS_1,
    UBUNTU_SUCCESS_2,
    WINDOWS7SP1_SUCCESS,
)


PING_FEDORA_EMPTY_BODY = b"""\
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.

--- 192.168.0.1 ping statistics ---
"""
PING_WINDOWS_INVALID = b"""\
Pinging 192.168.207.100 with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.207.100:
"""

DEBIAN_UNREACHABLE_0 = PingTestData(
    dedent(
        """\
        PING 192.168.207.100 (192.168.207.100) 56(84) bytes of data.

        --- 192.168.207.100 ping statistics ---
        5 packets transmitted, 0 received, 100% packet loss, time 4009ms
        """
    ),
    {
        "destination": "192.168.207.100",
        "packet_transmit": 5,
        "packet_receive": 0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": None,
        "packet_loss_count": 5,
        "packet_loss_rate": 100.0,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)
DEBIAN_UNREACHABLE_1 = PingTestData(
    DEBIAN_UNREACHABLE_0.value + "\n", DEBIAN_UNREACHABLE_0.expected, []
)
DEBIAN_UNREACHABLE_2 = PingTestData(
    DEBIAN_UNREACHABLE_1.value + "\n", DEBIAN_UNREACHABLE_0.expected, []
)

# Ubuntu 18.04
UBUNTU_FAIL_0 = PingTestData(
    # ping -D -O <ip addr>
    dedent(
        """\
        PING 192.168.11.222 (192.168.11.222) 56(84) bytes of data.
        [1596881133.081556] no answer yet for icmp_seq=1
        [1596881133.081898] 64 bytes from 192.168.11.222: icmp_seq=2 ttl=64 time=0.262 ms
        [1596881135.129517] no answer yet for icmp_seq=3
        [1596881136.153055] no answer yet for icmp_seq=4
        [1596881137.180056] no answer yet for icmp_seq=5
        [1596881137.180326] 64 bytes from 192.168.11.222: icmp_seq=6 ttl=64 time=0.221 ms
        [1596881138.201538] 64 bytes from 192.168.11.222: icmp_seq=7 ttl=64 time=0.257 ms
        ^C
        --- 192.168.11.222 ping statistics ---
        8 packets transmitted, 3 received, 62.5% packet loss, time 154ms
        """
    ),
    {
        "destination": "192.168.11.222",
        "packet_transmit": 8,
        "packet_receive": 3,
        "packet_loss_count": 5,
        "packet_loss_rate": 62.5,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0.0,
    },
    [
        {
            "timestamp": datetime(2020, 8, 8, 10, 5, 33, 81556, tzinfo=pytz.UTC),
            "icmp_seq": 1,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.11.222",
            "timestamp": datetime(2020, 8, 8, 10, 5, 33, 81898, tzinfo=pytz.UTC),
            "icmp_seq": 2,
            "ttl": 64,
            "time": 0.262,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2020, 8, 8, 10, 5, 35, 129517, tzinfo=pytz.UTC),
            "icmp_seq": 3,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2020, 8, 8, 10, 5, 36, 153055, tzinfo=pytz.UTC),
            "icmp_seq": 4,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2020, 8, 8, 10, 5, 37, 180056, tzinfo=pytz.UTC),
            "icmp_seq": 5,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.11.222",
            "timestamp": datetime(2020, 8, 8, 10, 5, 37, 180326, tzinfo=pytz.UTC),
            "icmp_seq": 6,
            "ttl": 64,
            "time": 0.221,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.11.222",
            "timestamp": datetime(2020, 8, 8, 10, 5, 38, 201538, tzinfo=pytz.UTC),
            "icmp_seq": 7,
            "ttl": 64,
            "time": 0.257,
            "duplicate": False,
        },
    ],
)

FEDORA_DUP_LOSS = PingTestData(
    dedent(
        """\
        PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.

        --- 192.168.0.1 ping statistics ---
        1688 packets transmitted, 1553 received, +1 duplicates, 7% packet loss, time 2987ms
        rtt min/avg/max/mdev = 0.282/0.642/11.699/0.699 ms, pipe 2, ipg/ewma 1.770/0.782 ms
        """
    ),
    {
        "destination": "192.168.0.1",
        "packet_transmit": 1688,
        "packet_receive": 1553,
        "packet_duplicate_count": 1,
        "packet_duplicate_rate": 0.0643915003219575,
        "packet_loss_count": 135,
        "packet_loss_rate": 7.9976303317535535,
        "rtt_min": 0.282,
        "rtt_max": 11.699,
        "rtt_mdev": 0.699,
        "rtt_avg": 0.642,
    },
    [],
)
FEDORA_UNREACHABLE = PingTestData(
    dedent(
        """\
        PING 192.168.207.100 (192.168.207.100) 56(84) bytes of data.
        From 192.168.207.128 icmp_seq=1 Destination Host Unreachable
        From 192.168.207.128 icmp_seq=2 Destination Host Unreachable
        From 192.168.207.128 icmp_seq=3 Destination Host Unreachable
        From 192.168.207.128 icmp_seq=4 Destination Host Unreachable
        From 192.168.207.128 icmp_seq=5 Destination Host Unreachable

        --- 192.168.207.100 ping statistics ---
        5 packets transmitted, 0 received, +5 errors, 100% packet loss, time 4003ms
        """
    ),
    {
        "destination": "192.168.207.100",
        "packet_transmit": 5,
        "packet_receive": 0,
        "packet_loss_count": 5,
        "packet_loss_rate": 100.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": None,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)

MACOS_SUCCESS_0 = PingTestData(
    dedent(
        """\
        PING google.com (172.217.6.238): 56 data bytes
        64 bytes from 172.217.6.238: icmp_seq=0 ttl=53 time=20.482 ms
        64 bytes from 172.217.6.238: icmp_seq=1 ttl=53 time=32.550 ms
        64 bytes from 172.217.6.238: icmp_seq=2 ttl=53 time=32.013 ms
        64 bytes from 172.217.6.238: icmp_seq=3 ttl=53 time=28.498 ms
        64 bytes from 172.217.6.238: icmp_seq=4 ttl=53 time=46.093 ms

        --- google.com ping statistics ---
        5 packets transmitted, 5 packets received, 0.0% packet loss
        round-trip min/avg/max/stddev = 20.482/31.927/46.093/8.292 ms
        """
    ),
    {
        "destination": "google.com",
        "packet_transmit": 5,
        "packet_receive": 5,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0,
        "rtt_min": 20.482,
        "rtt_avg": 31.927,
        "rtt_max": 46.093,
        "rtt_mdev": 8.292,
    },
    [
        {
            "bytes": 64,
            "destination": "172.217.6.238",
            "icmp_seq": 0,
            "ttl": 53,
            "time": 20.482,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "172.217.6.238",
            "icmp_seq": 1,
            "ttl": 53,
            "time": 32.55,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "172.217.6.238",
            "icmp_seq": 2,
            "ttl": 53,
            "time": 32.013,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "172.217.6.238",
            "icmp_seq": 3,
            "ttl": 53,
            "time": 28.498,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "172.217.6.238",
            "icmp_seq": 4,
            "ttl": 53,
            "time": 46.093,
            "duplicate": False,
        },
    ],
)
MACOS_SUCCESS_1 = PingTestData(
    dedent(
        """\
        PING github.com (192.30.255.113): 56 data bytes

        --- github.com ping statistics ---
        10 packets transmitted, 10 packets received, 0.0% packet loss
        round-trip min/avg/max/stddev = 218.391/283.477/405.879/70.170 ms
        """
    ),
    {
        "destination": "github.com",
        "packet_transmit": 10,
        "packet_receive": 10,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0,
        "rtt_min": 218.391,
        "rtt_avg": 283.477,
        "rtt_max": 405.879,
        "rtt_mdev": 70.170,
    },
    [],
)
MACOS_UNREACHABLE_0 = PingTestData(
    dedent(
        """\
        PING twitter.com (59.24.3.173): 56 data bytes
        ^C
        --- twitter.com ping statistics ---
        59 packets transmitted, 0 packets received, 100.0% packet loss
        """
    ),
    {
        "destination": "twitter.com",
        "packet_transmit": 59,
        "packet_receive": 0,
        "packet_loss_rate": 100.0,
        "packet_loss_count": 59,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
        "packet_duplicate_rate": None,
        "packet_duplicate_count": 0,
    },
    [],
)
MACOS_UNREACHABLE_1 = PingTestData(
    dedent(
        """\
        PING twitter.com (31.13.78.66): 56 data bytes

        --- twitter.com ping statistics ---
        10 packets transmitted, 0 packets received, 100.0% packet loss
        """
    ),
    {
        "destination": "twitter.com",
        "packet_transmit": 10,
        "packet_receive": 0,
        "packet_loss_count": 10,
        "packet_loss_rate": 100.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": None,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)
MACOS_UNREACHABLE_2 = PingTestData(
    dedent(
        """\
        PING example.net (93.184.216.34): 56 data bytes

        --- example.net ping statistics ---
        10 packets transmitted, 0 packets received, 100.0% packet loss
        """
    ),
    {
        "destination": "example.net",
        "packet_transmit": 10,
        "packet_receive": 0,
        "packet_loss_count": 10,
        "packet_loss_rate": 100.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": None,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)
MACOS_DUPLICATE_0 = PingTestData(
    dedent(
        """\
        PING duplicate.com (31.13.78.66): 56 data bytes

        --- duplicate.com ping statistics ---
        3 packets transmitted, 3 packets received, +3 duplicates, 0% packet loss

        round-trip min/avg/max/stddev = 0.311/1.091/2.186/0.662 ms
        """
    ),
    {
        "destination": "duplicate.com",
        "packet_transmit": 3,
        "packet_receive": 3,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_count": 3,
        "packet_duplicate_rate": 100,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)

ALPINE_LINUX_SUCCESS = PingTestData(
    dedent(
        """\
        PING heise.de (193.99.144.80): 56 data bytes

        --- heise.de ping statistics ---
        5 packets transmitted, 5 packets received, 0% packet loss
        round-trip min/avg/max = 0.638/0.683/0.746 ms
        """
    ),
    {
        "destination": "heise.de",
        "packet_transmit": 5,
        "packet_receive": 5,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0,
        "rtt_min": 0.638,
        "rtt_avg": 0.683,
        "rtt_max": 0.746,
        "rtt_mdev": None,
    },
    [],
)
ALPINE_LINUX_DUP_LOSS = PingTestData(
    dedent(
        """\
        PING 192.168.2.106 (192.168.2.106): 56 data bytes
        64 bytes from 192.168.2.106: seq=0 ttl=64 time=0.936 ms
        64 bytes from 192.168.2.106: seq=0 ttl=64 time=1.003 ms (DUP!)
        64 bytes from 192.168.2.106: seq=1 ttl=64 time=0.802 ms
        64 bytes from 192.168.2.106: seq=2 ttl=64 time=0.696 ms
        64 bytes from 192.168.2.106: seq=3 ttl=64 time=0.664 ms
        64 bytes from 192.168.2.106: seq=4 ttl=64 time=1.194 ms
        64 bytes from 192.168.2.106: seq=5 ttl=64 time=0.613 ms
        64 bytes from 192.168.2.106: seq=6 ttl=64 time=0.898 ms
        64 bytes from 192.168.2.106: seq=8 ttl=64 time=1.066 ms
        64 bytes from 192.168.2.106: seq=9 ttl=64 time=1.144 ms
        64 bytes from 192.168.2.106: seq=9 ttl=64 time=1.219 ms (DUP!)

        --- 192.168.2.106 ping statistics ---
        10 packets transmitted, 9 packets received, 2 duplicates, 10% packet loss
        round-trip min/avg/max = 0.613/0.930/1.219 ms
        """
    ),
    {
        "destination": "192.168.2.106",
        "packet_transmit": 10,
        "packet_receive": 9,
        "packet_duplicate_count": 2,
        "packet_duplicate_rate": 22.22222222222222,
        "packet_loss_count": 1,
        "packet_loss_rate": 10.0,
        "rtt_min": 0.613,
        "rtt_avg": 0.93,
        "rtt_max": 1.219,
        "rtt_mdev": None,
    },
    [
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 0,
            "ttl": 64,
            "time": 0.936,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 0,
            "ttl": 64,
            "time": 1.003,
            "duplicate": True,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 1,
            "ttl": 64,
            "time": 0.802,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 2,
            "ttl": 64,
            "time": 0.696,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 3,
            "ttl": 64,
            "time": 0.664,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 4,
            "ttl": 64,
            "time": 1.194,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 5,
            "ttl": 64,
            "time": 0.613,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 6,
            "ttl": 64,
            "time": 0.898,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 8,
            "ttl": 64,
            "time": 1.066,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 9,
            "ttl": 64,
            "time": 1.144,
            "duplicate": False,
        },
        {
            "bytes": 64,
            "destination": "192.168.2.106",
            "icmp_seq": 9,
            "ttl": 64,
            "time": 1.219,
            "duplicate": True,
        },
    ],
)

IPV6_LINUX = PingTestData(
    dedent(
        r"""\
        PING ff02::2%usb0(ff02::2%usb0) 56 data bytes
        64 bytes from fe80::783c:caff:fe12:b46c%usb0: icmp_seq=1 ttl=64 time=2.71 ms

        --- ff02::2%usb0 ping statistics ---
        1 packets transmitted, 1 received, 0% packet loss, time 0ms
        rtt min/avg/max/mdev = 2.708/2.708/2.708/0.000 ms
        """
    ),
    {
        "destination": r"ff02::2%usb0",
        "packet_transmit": 1,
        "packet_receive": 1,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "rtt_min": 2.708,
        "rtt_avg": 2.708,
        "rtt_max": 2.708,
        "rtt_mdev": 0.0,
    },
    [
        {
            "bytes": 64,
            "destination": r"fe80::783c:caff:fe12:b46c%usb0",
            "icmp_seq": 1,
            "ttl": 64,
            "time": 2.71,
            "duplicate": False,
        },
    ],
)

LINUX_PIPE = PingTestData(
    dedent(
        r"""\
        PING 91.221.122.179 (91.221.122.179) 64(92) bytes of data.
        [1622145167.999326] no answer yet for icmp_seq=1
        [1622145168.201746] no answer yet for icmp_seq=2
        [1622145168.405761] no answer yet for icmp_seq=3
        [1622145168.609750] no answer yet for icmp_seq=4
        [1622145170.826836] From 91.221.122.179 icmp_seq=1 Destination Host Unreachable
        [1622145170.826888] From 91.221.122.179 icmp_seq=2 Destination Host Unreachable
        [1622145170.826896] From 91.221.122.179 icmp_seq=3 Destination Host Unreachable
        [1622145170.826901] From 91.221.122.179 icmp_seq=4 Destination Host Unreachable
        [1622145170.826907] From 91.221.122.179 icmp_seq=5 Destination Host Unreachable

        --- 91.221.122.179 ping statistics ---
        5 packets transmitted, 0 received, +5 errors, 100% packet loss, time 811ms
        pipe 5
        """
    ),
    {
        "destination": "91.221.122.179",
        "packet_transmit": 5,
        "packet_receive": 0,
        "packet_loss_count": 5,
        "packet_loss_rate": 100.0,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": None,
    },
    [
        {
            "timestamp": datetime(2021, 5, 27, 19, 52, 47, 999326, tzinfo=pytz.UTC),
            "icmp_seq": 1,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2021, 5, 27, 19, 52, 48, 201746, tzinfo=pytz.UTC),
            "icmp_seq": 2,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2021, 5, 27, 19, 52, 48, 405761, tzinfo=pytz.UTC),
            "icmp_seq": 3,
            "duplicate": False,
        },
        {
            "timestamp": datetime(2021, 5, 27, 19, 52, 48, 609750, tzinfo=pytz.UTC),
            "icmp_seq": 4,
            "duplicate": False,
        },
    ],
)

WINDOWS10_LOSS = PingTestData(
    dedent(
        """\
        Pinging 192.168.2.106 with 32 bytes of data:
        Reply from 192.168.2.106: bytes=32 time=16ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=6ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=12ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=16ms TTL=64
        Request timed out.
        Reply from 192.168.2.106: bytes=32 time=8ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=33ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=13ms TTL=64
        Reply from 192.168.2.106: bytes=32 time=23ms TTL=64
        Reply from 192.168.2.106: bytes=32 time<1ms TTL=64

        Ping statistics for 192.168.2.106:
            Packets: Sent = 10, Received = 9, Lost = 1 (10% los
        Approximate round trip times in milli-seconds:
            Minimum = 0ms, Maximum = 33ms, Average = 14ms
        """
    ),
    {
        "destination": "192.168.2.106",
        "packet_transmit": 10,
        "packet_receive": 9,
        "packet_loss_count": 1,
        "packet_loss_rate": 10.0,
        "packet_duplicate_count": None,
        "packet_duplicate_rate": None,
        "rtt_min": 0.0,
        "rtt_avg": 14.0,
        "rtt_max": 33.0,
        "rtt_mdev": None,
    },
    [
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 16.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 6.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 12.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 16.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 8.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 33.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 13.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 23.0, "duplicate": False},
        {"bytes": 32, "destination": "192.168.2.106", "ttl": 64, "time": 1.0, "duplicate": False},
    ],
)
WINDOWS_UNREACHABLE_0 = PingTestData(
    dedent(
        """\
        Pinging 192.168.207.100 with 32 bytes of data:
        Request timed out.
        Request timed out.
        Request timed out.
        Request timed out.

        Ping statistics for 192.168.207.100:
            Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
        """
    ),
    {
        "destination": "192.168.207.100",
        "packet_transmit": 4,
        "packet_receive": 0,
        "packet_loss_count": 4,
        "packet_loss_rate": 100.0,
        "packet_duplicate_count": None,
        "packet_duplicate_rate": None,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None,
    },
    [],
)
WINDOWS_UNREACHABLE_1 = PingTestData(
    WINDOWS_UNREACHABLE_0.value + "\n", WINDOWS_UNREACHABLE_0.expected, []
)
WINDOWS_UNREACHABLE_2 = PingTestData(
    WINDOWS_UNREACHABLE_1.value + "\n", WINDOWS_UNREACHABLE_0.expected, []
)


class Test_PingParsing_parse:
    @pytest.mark.parametrize(
        ["test_data", "parser_name"],
        [
            [DEBIAN_SUCCESS_0, "Linux"],
            [DEBIAN_UNREACHABLE_0, "Linux"],
            [DEBIAN_UNREACHABLE_1, "Linux"],
            [DEBIAN_UNREACHABLE_2, "Linux"],
            [UBUNTU_SUCCESS_0, "Linux"],
            [UBUNTU_FAIL_0, "Linux"],
            [FEDORA_DUP_LOSS, "Linux"],
            [FEDORA_UNREACHABLE, "Linux"],
            [MACOS_SUCCESS_0, "macOS"],
            [MACOS_SUCCESS_1, "macOS"],
            [MACOS_UNREACHABLE_0, "macOS"],
            [MACOS_UNREACHABLE_1, "macOS"],
            [MACOS_UNREACHABLE_2, "macOS"],
            [MACOS_DUPLICATE_0, "macOS"],
            [ALPINE_LINUX_SUCCESS, "AlpineLinux"],
            [ALPINE_LINUX_DUP_LOSS, "AlpineLinux"],
            [WINDOWS7SP1_SUCCESS, "Windows"],
            [WINDOWS10_LOSS, "Windows"],
            [WINDOWS_UNREACHABLE_0, "Windows"],
            [WINDOWS_UNREACHABLE_1, "Windows"],
            [WINDOWS_UNREACHABLE_2, "Windows"],
            [IPV6_LINUX, "Linux"],
            [LINUX_PIPE, "Linux"],
        ],
    )
    def test_normal_text(self, ping_parser, test_data, parser_name):
        stats = ping_parser.parse(test_data.value)

        print(f"[input text]\n{test_data.value}\n")
        print(f"[expected]\n{test_data.expected}\n")
        print(f"[actual]\n{stats.as_dict()}\n")
        for icmp_reply in stats.icmp_replies:
            print(icmp_reply)

        assert ping_parser.parser_name == parser_name
        assert stats.as_dict() == test_data.expected
        assert stats.icmp_replies == test_data.replies

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(
        ["test_data", "parser_name"], [[UBUNTU_SUCCESS_1, "Linux"], [UBUNTU_SUCCESS_2, "Linux"]]
    )
    def test_normal_timestamp(self, ping_parser, test_data, parser_name):
        stats = ping_parser.parse(test_data.value)

        print(f"[input text]\n{test_data.value}\n")
        print(f"[expected]\n{test_data.expected}\n")
        print(f"[actual]\n{stats.as_dict()}\n")
        for icmp_reply in stats.icmp_replies:
            print(icmp_reply)

        assert ping_parser.parser_name == parser_name
        assert stats.as_dict() == test_data.expected
        assert stats.icmp_replies == test_data.replies

    def test_empty(self, ping_parser):
        ping_parser.parse(
            dedent(
                """\
            PING google.com (216.58.196.238) 56(84) bytes of data.

            --- google.com ping statistics ---
            60 packets transmitted, 60 received, 0% packet loss, time 59153ms
            rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
            """
            )
        )
        stats = ping_parser.parse("")

        assert stats.is_empty()

    @pytest.mark.parametrize(
        ["value"],
        [
            [
                PingResult(
                    stdout="",
                    stderr="ping: unknown: Temporary failure in name resolution\n",
                    returncode=2,
                )
            ]
        ],
    )
    def test_ping_failure(self, ping_parser, value):
        stats = ping_parser.parse(value)
        assert stats.is_empty()

    @pytest.mark.parametrize(
        ["value", "expected"],
        [[PING_FEDORA_EMPTY_BODY, ParseError], [PING_WINDOWS_INVALID, ParseError]],
    )
    def test_exception(self, ping_parser, value, expected):
        with pytest.raises(expected):
            ping_parser.parse(value)


class Test_PingParsing_as_tuple:
    def test_normal(self, ping_parser):
        stats = ping_parser.parse(DEBIAN_SUCCESS_0.value)
        result = stats.as_tuple()

        assert result.destination == "google.com"
        assert result.packet_transmit == 60
        assert result.packet_receive == 60
        assert result.packet_loss_count == 0
        assert result.packet_loss_rate == 0.0
        assert result.packet_duplicate_rate == 0
        assert result.packet_duplicate_count == 0
        assert result.rtt_min == 61.425
        assert result.rtt_avg == 99.731
        assert result.rtt_max == 212.597
        assert result.rtt_mdev == 27.566
        assert stats.icmp_replies == []
