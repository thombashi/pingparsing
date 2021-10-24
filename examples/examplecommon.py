#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import json


def print_ping_parser(ping_parser):
    print("# properties ---")
    print(f"packet_transmit: {ping_parser.packet_transmit:d} packets")
    print(f"packet_receive: {ping_parser.packet_receive:d} packets")
    print(f"packet_loss_rate: {ping_parser.packet_loss_rate:.1f} %")
    print(f"packet_loss_count: {ping_parser.packet_loss_count:d} packets")

    if ping_parser.packet_duplicate_rate:
        packet_duplicate_rate = f"{ping_parser.packet_duplicate_rate:.1f} %"
    else:
        packet_duplicate_rate = "NaN"
    print(f"packet_duplicate_rate: {packet_duplicate_rate:s}")

    if ping_parser.packet_duplicate_count:
        packet_duplicate_count = f"{ping_parser.packet_duplicate_count:d} packets"
    else:
        packet_duplicate_count = "NaN"
    print(f"packet_duplicate_count: {packet_duplicate_count:s}")

    print("rtt_min:", ping_parser.rtt_min)
    print("rtt_avg:", ping_parser.rtt_avg)
    print("rtt_max:", ping_parser.rtt_max)
    print("rtt_mdev:", ping_parser.rtt_mdev)
    print()
    print("# as_dict ---")
    print(json.dumps(ping_parser.as_dict(), indent=4))
