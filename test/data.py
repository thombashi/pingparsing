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
