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
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = "google.com"
    transmitter.count = 10
    result = transmitter.ping()

    print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
