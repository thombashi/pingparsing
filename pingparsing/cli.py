#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import argparse
import multiprocessing
import os
import sys
from datetime import datetime
from textwrap import dedent

import humanreadable as hr
import logbook
import six
from subprocrunner import CommandError

from .__version__ import __version__
from ._logger import set_log_level
from ._pingparsing import PingParsing
from ._pingtransmitter import PingTransmitter


try:
    import simplejson as json
except ImportError:
    import json


DEFAULT_COUNT = 10
QUIET_LOG_LEVEL = logbook.NOTSET
TIMESTAMP_TYPES = (int, float, six.text_type)


class TimestampFormat(object):
    NONE = "none"
    EPOCH = "epoch"
    DATETIME = "datetime"
    LIST = (NONE, EPOCH, DATETIME)


def _get_unit_help_msg():
    return ", ".join(["/".join(values) for values in hr.Time.get_text_units().values()])


def parse_option():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Documentation: https://pingparsing.rtfd.io/
            Issue tracker: https://github.com/thombashi/pingparsing/issues
            """
        ),
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    use_stdin, found_stdin_specifier = is_use_stdin()
    if not use_stdin or found_stdin_specifier:
        parser.add_argument(
            "destination_or_file",
            nargs="+",
            help="Destinations to send ping, or files to parse. '-' for parse the standard input.",
        )

    parser.add_argument(
        "--max-workers",
        type=int,
        help="""Number of threads for when multiple destination/file
        specified. defaults to equals to two times number of cores.
        """,
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=4,
        help="""JSON output will be pretty-printed with the indent level.
        (default= %(default)s)
        """,
    )
    parser.add_argument(
        "--icmp-reply",
        "--icmp-replies",
        action="store_true",
        default=False,
        help="print results for each ICMP packet reply.",
    )

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=logbook.DEBUG,
        default=logbook.INFO,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=QUIET_LOG_LEVEL,
        default=logbook.INFO,
        help="suppress execution log messages.",
    )

    group = parser.add_argument_group("Ping Options")
    group.add_argument(
        "--timestamp",
        choices=TimestampFormat.LIST,
        default=TimestampFormat.NONE,
        help="""[Only for LINUX]
        {}: no timestamps.
        {}: add timestamps with UNIX epoch time format.
        {}: add timestamps with ISO time format.
        """.format(
            TimestampFormat.NONE, TimestampFormat.EPOCH, TimestampFormat.DATETIME
        ),
    )
    group.add_argument(
        "-c",
        "--count",
        type=int,
        help="""Stop after sending the count.
        see also ping(8) [-c count] option description.
        """,
    )
    group.add_argument(
        "-w",
        "--deadline",
        type=str,
        help="""Timeout before ping exits.
        valid time units are: {units}. if no unit string found, considered seconds as
        the time unit.

        see also ping(8) [-w deadline] option description.
        note: meaning of the 'deadline' may differ system to system.
        """.format(
            units=_get_unit_help_msg()
        ),
    )
    group.add_argument(
        "--timeout",
        type=str,
        help="""Time to wait for a response per packet.
        Valid time units are: {units}. if no unit string found, considered milliseconds as
        the time unit.
        Attempt to send packets with milliseconds granularity in default.
        If the system does not support timeout in milliseconds, round up as seconds.
        Use system default if not specified.
        This option will be ignored if the system does not support timeout itself.

        See also ping(8) [-W timeout] option description.
        note: meaning of the 'timeout' may differ system to system.
        """.format(
            units=_get_unit_help_msg()
        ),
    )
    group.add_argument("-I", "--interface", dest="interface", help="network interface")

    return parser.parse_args()


def initialize_log_handler(log_level):
    from logbook.more import ColorizedStderrHandler

    debug_level_format_str = (
        "[{record.level_name}] {record.channel} {record.func_name} "
        "({record.lineno}): {record.message}"
    )
    if log_level == logbook.DEBUG:
        info_level_format_str = debug_level_format_str
    else:
        info_level_format_str = "[{record.level_name}] {record.channel}: {record.message}"

    ColorizedStderrHandler(
        level=logbook.DEBUG, format_string=debug_level_format_str
    ).push_application()
    ColorizedStderrHandler(
        level=logbook.INFO, format_string=info_level_format_str
    ).push_application()


def is_use_stdin():
    if sys.stdin.isatty():
        return (False, False)

    found_stdin_specifier = "-" in sys.argv[1:]

    return (len(sys.argv) == 1 or found_stdin_specifier, found_stdin_specifier)


def parse_ping(
    logger, dest_or_file, interface, count, deadline, timeout, is_parse_icmp_reply, timestamp
):
    if os.path.isfile(dest_or_file):
        with open(dest_or_file) as f:
            ping_result_text = f.read()
    else:
        transmitter = PingTransmitter()
        transmitter.destination = dest_or_file
        transmitter.interface = interface
        transmitter.count = count
        transmitter.deadline = deadline
        transmitter.timeout = timeout
        transmitter.is_quiet = not is_parse_icmp_reply
        transmitter.timestamp = timestamp != TimestampFormat.NONE

        try:
            result = transmitter.ping()
        except CommandError as e:
            logger.error(e)
            sys.exit(e.errno)

        ping_result_text = result.stdout
        if result.returncode != 0:
            if result.stderr:
                logger.error(result.stderr)

    ping_parser = PingParsing()
    stats = ping_parser.parse(ping_result_text)
    output = stats.as_dict()
    if is_parse_icmp_reply:
        output["icmp_replies"] = stats.icmp_replies

    return (dest_or_file, output)


def get_ping_param(options):
    count = options.count
    deadline = options.deadline
    timeout = options.timeout

    if not options.count and not options.deadline:
        count = DEFAULT_COUNT

    return (count, deadline, timeout)


def print_result(text):
    if not sys.stdout.isatty():
        # avoid to colorized when piped or redirected
        print(text)
        return

    try:
        from pygments import highlight
        from pygments.lexers import JsonLexer
        from pygments.formatters import TerminalTrueColorFormatter

        print(
            highlight(
                code=text, lexer=JsonLexer(), formatter=TerminalTrueColorFormatter(style="monokai")
            ).strip()
        )
    except ImportError:
        print(text)


def _serialize_epoch(obj):
    if isinstance(obj, datetime):
        return float(obj.strftime("%s.%f"))

    if isinstance(obj, TIMESTAMP_TYPES):
        return obj

    raise TypeError("not supported type to convert: {}".format(type(obj)))


def _serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, TIMESTAMP_TYPES):
        return obj

    raise TypeError("not supported type to convert: {}".format(type(obj)))


timestamp_serialize_map = {
    TimestampFormat.NONE: None,
    TimestampFormat.EPOCH: _serialize_epoch,
    TimestampFormat.DATETIME: _serialize_datetime,
}


def dumps_dict(obj, timestamp_format, indent=0):
    serialize_func = timestamp_serialize_map[timestamp_format]

    if indent <= 0:
        return json.dumps(obj, default=serialize_func)

    return json.dumps(obj, indent=indent, default=serialize_func)


def main():
    options = parse_option()

    initialize_log_handler(options.log_level)

    logger = logbook.Logger("pingparsing cli")
    logger.level = options.log_level
    set_log_level(options.log_level)

    output = {}
    use_stdin, found_stdin_specifier = is_use_stdin()
    if not use_stdin and not found_stdin_specifier:
        from concurrent import futures

        max_workers = (
            multiprocessing.cpu_count() * 2 if options.max_workers is None else options.max_workers
        )
        count, deadline, timeout = get_ping_param(options)
        logger.debug(
            "max-workers={}, count={}, deadline={}, timeout={}".format(
                max_workers, count, deadline, timeout
            )
        )

        try:
            with futures.ProcessPoolExecutor(max_workers) as executor:
                future_list = []
                for dest_or_file in options.destination_or_file:
                    logger.debug("start {}".format(dest_or_file))
                    future_list.append(
                        executor.submit(
                            parse_ping,
                            logger,
                            dest_or_file,
                            options.interface,
                            count,
                            deadline,
                            timeout,
                            options.icmp_reply,
                            options.timestamp,
                        )
                    )

                for future in futures.as_completed(future_list):
                    key, ping_data = future.result()
                    output[key] = ping_data
        finally:
            logger.debug("shutdown ProcessPoolExecutor")
            executor.shutdown()
    else:
        ping_result_text = sys.stdin.read()
        ping_parser = PingParsing()
        stats = ping_parser.parse(ping_result_text)
        output = stats.as_dict()
        if options.icmp_reply:
            output["icmp_replies"] = stats.icmp_replies

    print_result(dumps_dict(output, timestamp_format=options.timestamp, indent=options.indent))

    return 0


if __name__ == "__main__":
    sys.exit(main())
