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
    stats = parser.parse(dedent("""\
        PING twitter.com (104.244.42.65) 56(84) bytes of data.
        64 bytes from 104.244.42.65: icmp_seq=1 ttl=53 time=68.5 ms
        64 bytes from 104.244.42.65: icmp_seq=2 ttl=53 time=67.7 ms
        64 bytes from 104.244.42.65: icmp_seq=3 ttl=53 time=65.6 ms
        64 bytes from 104.244.42.65: icmp_seq=4 ttl=53 time=65.6 ms
        64 bytes from 104.244.42.65: icmp_seq=5 ttl=53 time=64.9 ms

        --- twitter.com ping statistics ---
        5 packets transmitted, 5 received, 0% packet loss, time 4003ms
        rtt min/avg/max/mdev = 64.912/66.494/68.524/1.430 ms
        """))

    print("[ping statistics]")
    print(json.dumps(stats.as_dict(), indent=4))

    print("\n[icmp reply]")
    for icmp_reply in stats.icmp_reply_list:
        print(icmp_reply)

    return 0


if __name__ == "__main__":
    sys.exit(main())
