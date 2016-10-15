#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
import json


def print_ping_parser(ping_parser):
    print("# properties ---")
    print("packet_transmit: {:d} packets".format(ping_parser.packet_transmit))
    print("packet_receive: {:d} packets".format(ping_parser.packet_receive))
    print("packet_loss: {:.1f} %".format(ping_parser.packet_loss))
    print("rtt_min:", ping_parser.rtt_min)
    print("rtt_avg:", ping_parser.rtt_avg)
    print("rtt_max:", ping_parser.rtt_max)
    print("rtt_mdev:", ping_parser.rtt_mdev)
    print()
    print("# asdict ---")
    print(json.dumps(ping_parser.as_dict(), indent=4))
