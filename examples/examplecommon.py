#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import json


def print_ping_parser(ping_parser):
    print("# properties ---")
    print("packet_transmit: {:d} packets".format(ping_parser.packet_transmit))
    print("packet_receive: {:d} packets".format(ping_parser.packet_receive))
    print("packet_loss_rate: {:.1f} %".format(ping_parser.packet_loss_rate))
    print("packet_loss_count: {:d} packets".format(ping_parser.packet_loss_count))

    if ping_parser.packet_duplicate_rate:
        packet_duplicate_rate = "{:.1f} %".format(ping_parser.packet_duplicate_rate)
    else:
        packet_duplicate_rate = "NaN"
    print("packet_duplicate_rate: {:s}".format(packet_duplicate_rate))

    if ping_parser.packet_duplicate_count:
        packet_duplicate_count = "{:d} packets".format(ping_parser.packet_duplicate_count)
    else:
        packet_duplicate_count = "NaN"
    print("packet_duplicate_count: {:s}".format(packet_duplicate_count))

    print("rtt_min:", ping_parser.rtt_min)
    print("rtt_avg:", ping_parser.rtt_avg)
    print("rtt_max:", ping_parser.rtt_max)
    print("rtt_mdev:", ping_parser.rtt_mdev)
    print()
    print("# as_dict ---")
    print(json.dumps(ping_parser.as_dict(), indent=4))
