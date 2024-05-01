"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from datetime import datetime
from textwrap import dedent

import pytz

from .common import PingTestData


# ping google.com -q -c 60:
#   - Debian 8.2 w/ iputils-ping 20121221-5+b2
PING_DEBIAN_SUCCESS_0 = b"""\
PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
"""
DEBIAN_SUCCESS_0 = PingTestData(
    PING_DEBIAN_SUCCESS_0,
    {
        "destination": "google.com",
        "packet_transmit": 60,
        "packet_receive": 60,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_rate": 0,
        "packet_duplicate_count": 0,
        "rtt_min": 61.425,
        "rtt_avg": 99.731,
        "rtt_max": 212.597,
        "rtt_mdev": 27.566,
    },
    [],
)


# Ubuntu 16.04
#   $ ping -c 5 twitter.com
PING_UBUNTU_SUCCESS_0 = b"""\
PING twitter.com (104.244.42.65) 56(84) bytes of data.
64 bytes from 104.244.42.65: icmp_seq=1 ttl=53 time=68.5 ms
64 bytes from 104.244.42.65: icmp_seq=2 ttl=53 time=67.7 ms
64 bytes from 104.244.42.65: icmp_seq=3 ttl=53 time=65.6 ms
64 bytes from 104.244.42.65: icmp_seq=4 ttl=53 time=65.6 ms
64 bytes from 104.244.42.65: icmp_seq=5 ttl=53 time=64.9 ms

--- twitter.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4003ms
rtt min/avg/max/mdev = 64.912/66.494/68.524/1.430 ms
"""
UBUNTU_SUCCESS_0 = PingTestData(
    PING_UBUNTU_SUCCESS_0,
    {
        "destination": "twitter.com",
        "packet_transmit": 5,
        "packet_receive": 5,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_rate": 0,
        "packet_duplicate_count": 0,
        "rtt_min": 64.912,
        "rtt_avg": 66.494,
        "rtt_max": 68.524,
        "rtt_mdev": 1.430,
    },
    [
        {
            "destination": "104.244.42.65",
            "bytes": 64,
            "icmp_seq": 1,
            "ttl": 53,
            "time": 68.5,
            "duplicate": False,
        },
        {
            "destination": "104.244.42.65",
            "bytes": 64,
            "icmp_seq": 2,
            "ttl": 53,
            "time": 67.7,
            "duplicate": False,
        },
        {
            "destination": "104.244.42.65",
            "bytes": 64,
            "icmp_seq": 3,
            "ttl": 53,
            "time": 65.6,
            "duplicate": False,
        },
        {
            "destination": "104.244.42.65",
            "bytes": 64,
            "icmp_seq": 4,
            "ttl": 53,
            "time": 65.6,
            "duplicate": False,
        },
        {
            "destination": "104.244.42.65",
            "bytes": 64,
            "icmp_seq": 5,
            "ttl": 53,
            "time": 64.9,
            "duplicate": False,
        },
    ],
)

# Ubuntu 16.04
#   $ ping -c 5 google.com -D
PING_UBUNTU_SUCCESS_1 = b"""\
PING google.com (74.125.24.100) 56(84) bytes of data.
[1524930937.003555] 64 bytes from 74.125.24.100: icmp_seq=1 ttl=39 time=148 ms
[1524930937.787175] 64 bytes from 74.125.24.100: icmp_seq=2 ttl=39 time=137 ms
[1524930938.787642] 64 bytes from 74.125.24.100: icmp_seq=3 ttl=39 time=137 ms
[1524930939.787653] 64 bytes from 74.125.24.100: icmp_seq=4 ttl=39 time=136 ms
[1524930940.788365] 64 bytes from 74.125.24.100: icmp_seq=5 ttl=39 time=136 ms

--- google.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4001ms
rtt min/avg/max/mdev = 136.537/139.174/148.006/4.425 ms
"""
UBUNTU_SUCCESS_1 = PingTestData(
    PING_UBUNTU_SUCCESS_1,
    {
        "destination": "google.com",
        "packet_transmit": 5,
        "packet_receive": 5,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_rate": 0,
        "packet_duplicate_count": 0,
        "rtt_min": 136.537,
        "rtt_avg": 139.174,
        "rtt_max": 148.006,
        "rtt_mdev": 4.425,
    },
    [
        {
            "destination": "74.125.24.100",
            "bytes": 64,
            "timestamp": datetime(2018, 4, 28, 15, 55, 37, 3555, tzinfo=pytz.UTC),
            "icmp_seq": 1,
            "ttl": 39,
            "time": 148.0,
            "duplicate": False,
        },
        {
            "destination": "74.125.24.100",
            "bytes": 64,
            "timestamp": datetime(2018, 4, 28, 15, 55, 37, 787175, tzinfo=pytz.UTC),
            "icmp_seq": 2,
            "ttl": 39,
            "time": 137.0,
            "duplicate": False,
        },
        {
            "destination": "74.125.24.100",
            "bytes": 64,
            "timestamp": datetime(2018, 4, 28, 15, 55, 38, 787642, tzinfo=pytz.UTC),
            "icmp_seq": 3,
            "ttl": 39,
            "time": 137.0,
            "duplicate": False,
        },
        {
            "destination": "74.125.24.100",
            "bytes": 64,
            "timestamp": datetime(2018, 4, 28, 15, 55, 39, 787653, tzinfo=pytz.UTC),
            "icmp_seq": 4,
            "ttl": 39,
            "time": 136.0,
            "duplicate": False,
        },
        {
            "destination": "74.125.24.100",
            "bytes": 64,
            "timestamp": datetime(2018, 4, 28, 15, 55, 40, 788365, tzinfo=pytz.UTC),
            "icmp_seq": 5,
            "ttl": 39,
            "time": 136.0,
            "duplicate": False,
        },
    ],
)

# Ubuntu 18.04
#   $ ping google.com -c 3
PING_UBUNTU_SUCCESS_2 = b"""\
PING google.com (172.217.26.110) 56(84) bytes of data.
64 bytes from kix05s01-in-f14.1e100.net (172.217.26.110): icmp_seq=1 ttl=50 time=64.3 ms
64 bytes from kix05s01-in-f14.1e100.net (172.217.26.110): icmp_seq=2 ttl=50 time=49.7 ms
64 bytes from kix05s01-in-f14.1e100.net (172.217.26.110): icmp_seq=3 ttl=50 time=48.8 ms

--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 48.832/54.309/64.334/7.098 ms
"""
UBUNTU_SUCCESS_2 = PingTestData(
    PING_UBUNTU_SUCCESS_2,
    {
        "destination": "google.com",
        "packet_transmit": 3,
        "packet_receive": 3,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_rate": 0,
        "packet_duplicate_count": 0,
        "rtt_min": 48.832,
        "rtt_avg": 54.309,
        "rtt_max": 64.334,
        "rtt_mdev": 7.098,
    },
    [
        {
            "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
            "bytes": 64,
            "icmp_seq": 1,
            "ttl": 50,
            "time": 64.3,
            "duplicate": False,
        },
        {
            "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
            "bytes": 64,
            "icmp_seq": 2,
            "ttl": 50,
            "time": 49.7,
            "duplicate": False,
        },
        {
            "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
            "bytes": 64,
            "icmp_seq": 3,
            "ttl": 50,
            "time": 48.8,
            "duplicate": False,
        },
    ],
)

WINDOWS7SP1_SUCCESS = PingTestData(
    # ping google.com -n 10:
    dedent(
        """\
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
        """
    ),
    {
        "destination": "216.58.196.238",
        "packet_transmit": 10,
        "packet_receive": 10,
        "packet_loss_count": 0,
        "packet_loss_rate": 0.0,
        "packet_duplicate_count": None,
        "packet_duplicate_rate": None,
        "rtt_min": 56,
        "rtt_avg": 107,
        "rtt_max": 194,
        "rtt_mdev": None,
    },
    [
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 87.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 97.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 56.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 95.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 194.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 98.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 93.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 96.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 96.0,
            "duplicate": False,
        },
        {
            "bytes": 32,
            "destination": "216.58.196.238",
            "ttl": 51,
            "time": 165.0,
            "duplicate": False,
        },
    ],
)
