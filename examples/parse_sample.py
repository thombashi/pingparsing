#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import json
import sys

import pingparsing


def main():
    parser = pingparsing.PingParsing()
    parser.parse("""PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")

    print(json.dumps(parser.as_dict(), indent=4))

    return 0


if __name__ == "__main__":
    sys.exit(main())
