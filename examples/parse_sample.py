#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import json
import sys
from textwrap import dedent

import pingparsing


def main():
    parser = pingparsing.PingParsing()
    stats = parser.parse(
        dedent(
            """\
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
        )
    )

    print("[ping statistics]")
    print(json.dumps(stats.as_dict(), indent=4))

    print("\n[icmp reply]")
    for icmp_reply in stats.icmp_reply_list:
        print(icmp_reply)

    return 0


if __name__ == "__main__":
    sys.exit(main())
