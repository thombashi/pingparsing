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
from textwrap import dedent

import logbook
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

    if is_use_stdin():
        parser.add_argument("destination_or_file", nargs="+", help="")

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
        "-c",
        "--count",
        type=int,
        help="""stop after sending the count.
        see also ping(8) [-c count] option description.
        """,
    )
    group.add_argument(
        "-w",
        "--deadline",
        type=float,
        help="""timeout in seconds.
        see also ping(8) [-w deadline] option description.
        note: meaning of the 'deadline' may differ system to system.
        """,
    )
    group.add_argument(
        "--timeout",
        type=float,
        help="""Time to wait for a response, in milliseconds.
        If the system does not support timeout in milliseconds, round up as seconds.
        Use system default if not specified.
        Ignored if the system does not support timeout itself.

        See also ping(8) [-W timeout] option description.
        note: meaning of the 'timeout' may differ system to system.
        """,
    )
    group.add_argument("-I", "--interface", dest="interface", help="network interface")

    return parser.parse_args()


def initialize_log_handler(log_level):
    debug_level_format_str = (
        "[{record.level_name}] {record.channel} {record.func_name} "
        "({record.lineno}): {record.message}"
    )
    if log_level == logbook.DEBUG:
        info_level_format_str = debug_level_format_str
    else:
        info_level_format_str = "[{record.level_name}] {record.channel}: {record.message}"

    logbook.StderrHandler(
        level=logbook.DEBUG, format_string=debug_level_format_str
    ).push_application()
    logbook.StderrHandler(
        level=logbook.INFO, format_string=info_level_format_str
    ).push_application()


def is_use_stdin():
    return sys.stdin.isatty() or len(sys.argv) > 1


def parse_ping(logger, dest_or_file, interface, count, deadline, timeout, is_parse_icmp_reply):
    if os.path.isfile(dest_or_file):
        with open(dest_or_file) as f:
            ping_result_text = f.read()
    else:
        transmitter = PingTransmitter()
        transmitter.destination_host = dest_or_file
        transmitter.interface = interface
        transmitter.count = count
        transmitter.deadline = deadline
        transmitter.timeout = timeout
        transmitter.is_quiet = not is_parse_icmp_reply

        try:
            result = transmitter.ping()
        except CommandError as e:
            logger.error(e)
            sys.exit(e.errno)

        ping_result_text = result.stdout
        if result.returncode != 0:
            logger.error(result.stderr)

    ping_parser = PingParsing()
    stats = ping_parser.parse(ping_result_text)
    output = stats.as_dict()
    if is_parse_icmp_reply:
        output["icmp_reply"] = stats.icmp_reply_list

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


def main():
    options = parse_option()

    initialize_log_handler(options.log_level)

    logger = logbook.Logger("pingparsing cli")
    logger.level = options.log_level
    set_log_level(options.log_level)

    output = {}
    if is_use_stdin():
        from concurrent import futures

        set_log_level(options.log_level)

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
            output["icmp_reply"] = stats.icmp_reply_list

    if options.indent <= 0:
        result = json.dumps(output)
    else:
        result = json.dumps(output, indent=options.indent)

    print_result(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
