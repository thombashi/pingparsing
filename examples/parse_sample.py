#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
import argparse
import sys

import examplecommon
import pingparsing


def parse_option():
    parser = argparse.ArgumentParser()
    parser .add_argument(
        "-f", "--file", required=True, help="input file path")

    return parser.parse_args()


def main():
    options = parse_option()

    ping_parser = pingparsing.PingParsing()
    with open(options.file) as f:
        ping_parser.parse(f.read())

    examplecommon.print_ping_parser(ping_parser)

    return 0


if __name__ == "__main__":
    sys.exit(main())
