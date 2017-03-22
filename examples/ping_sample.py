#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function

import argparse
import sys

import pingparsing

import examplecommon


def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--destination", required=True, help="destination host")
    parser.add_argument(
        "-I", dest="interface", help="interface")

    return parser.parse_args()


def main():
    options = parse_option()

    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination_host = options.destination
    transmitter.interface = options.interface
    transmitter.waittime = 10
    result = transmitter.ping()
    ping_parser.parse(result.stdout)

    print("# returncode ---")
    print(result.returncode)
    print()
    examplecommon.print_ping_parser(ping_parser)

    return 0


if __name__ == "__main__":
    sys.exit(main())
