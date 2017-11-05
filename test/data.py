# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import six

from .common import PingTestData

# ping google.com -q -c 60:
#   - Debian 8.2 w/ iputils-ping 20121221-5+b2
#   - Debian 5.0.10 w/ iputils-ping 20071127-1+lenny1
PING_DEBIAN_SUCCESS = six.b("""PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")


DEBIAN_SUCCESS = PingTestData(
    PING_DEBIAN_SUCCESS,
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
    })

WINDOWS7SP1_SUCCESS = PingTestData(
    # ping google.com -n 10:
    """
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
""",
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
    })
