"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import argparse
import multiprocessing
import os
import sys
from datetime import datetime
from textwrap import dedent
from typing import Any, Dict, Optional, Tuple

import humanreadable as hr
from pytz import timezone
from subprocrunner import CommandError

from .__version__ import __version__
from ._logger import logger, set_logger
from ._pingparsing import PingParsing
from ._pingtransmitter import PingTransmitter
from ._typing import PingAddOpts, TimeArg


try:
    import simplejson as json
except ImportError:
    import json  # type: ignore


DEFAULT_COUNT = 10
TIMESTAMP_TYPES = (int, float, str)


class TimestampFormat:
    NONE = "none"
    EPOCH = "epoch"
    DATETIME = "datetime"
    LIST = (NONE, EPOCH, DATETIME)


class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    QUIET = "QUIET"


def _get_unit_help_msg() -> str:
    return ", ".join(["/".join(values) for values in hr.Time.get_text_units().values()])


def parse_option() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Documentation: https://pingparsing.rtfd.io/
            Issue tracker: https://github.com/thombashi/pingparsing/issues
            """
        ),
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    use_stdin, found_stdin_specifier = is_use_stdin()
    if not use_stdin or found_stdin_specifier:
        parser.add_argument(
            "destination_or_file",
            nargs="+",
            help="Destinations to send ping or files to parse. '-' for parsing the standard input.",
        )

    parser.add_argument(
        "--max-workers",
        type=int,
        help="""Number of threads for when multiple destinations/files are specified.
        Defaults to equal two times the number of cores.
        """,
    )

    group = parser.add_argument_group("Ping Options")  # type: ignore
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
        "-s",
        "--packet-size",
        type=int,
        help="Specifies the number of data bytes to be sent.",
    )
    group.add_argument(
        "--ttl",
        type=int,
        help="Specifies the Time to Live.",
    )
    group.add_argument(
        "-w",
        "--deadline",
        type=str,
        help="""Timeout before ping exits.
        valid time units are: {units}. if no unit string found, considered seconds as
        the time unit.

        see also ping(8) [-w deadline] option description.
        note: meaning of the 'deadline' may differ system from to system.
        """.format(
            units=_get_unit_help_msg()
        ),
    )
    group.add_argument(
        "--timeout",
        type=str,
        help="""Time to wait for a response per packet.
        Valid time units are: {units}.
        If no unit string is found, consider milliseconds as the time unit.
        Attempt to send packets with milliseconds granularity in default.
        If the system does not support timeout in milliseconds, round up as seconds.
        Use system default if not specified.
        This option will be ignored if the system does not support timeout itself.

        See also ping(8) [-W timeout] option description.
        note: meaning of the 'timeout' may differ from system to system.
        """.format(
            units=_get_unit_help_msg()
        ),
    )
    group.add_argument("-I", "--interface", dest="interface", help="network interface")
    group.add_argument("--addopts", metavar="OPTIONS", help="extra command line options")

    group = parser.add_argument_group("Output Options")  # type: ignore
    group.add_argument(
        "--indent",
        type=int,
        default=4,
        help="""JSON output will be pretty-printed with the indent level.
        (default= %(default)s)
        """,
    )
    group.add_argument(
        "--icmp-reply",
        "--icmp-replies",
        action="store_true",
        default=False,
        help="print results for each ICMP packet reply.",
    )
    group.add_argument(
        "--timezone",
        help="Time zone for timestamps.",
    )
    group.add_argument(
        "--no-color",
        action="store_true",
        default=False,
        help="Turn off colors.",
    )

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()  # type: ignore
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.DEBUG,
        default=LogLevel.INFO,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.QUIET,
        default=LogLevel.INFO,
        help="suppress execution log messages.",
    )

    return parser.parse_args()


def initialize_logger(log_level: str) -> None:
    logger.remove()

    if log_level == LogLevel.QUIET:
        set_logger(is_enable=False)
        return

    if log_level == LogLevel.DEBUG:
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

        try:
            import loguru  # noqa
        except ImportError:
            print(
                "required to install with 'pip install pingparsing[cli]' to debug print",
                file=sys.stderr,
            )
    else:
        log_format = "<level>[{level}]</level> {message}"

    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level, enqueue=True)
    set_logger(is_enable=True)


def is_use_stdin() -> Tuple[bool, bool]:
    if sys.stdin.isatty():
        return (False, False)

    found_stdin_specifier = "-" in sys.argv[1:]

    return (len(sys.argv) == 1 or found_stdin_specifier, found_stdin_specifier)


def parse_ping(
    dest_or_file: str,
    interface: Optional[str],
    count: int,
    packet_size: Optional[int],
    ttl: Optional[int],
    deadline: TimeArg,
    timeout: TimeArg,
    is_parse_icmp_reply: bool,
    timestamp: str,
    timezone_name: str,
    addopts: PingAddOpts,
) -> Tuple[str, Any]:
    if os.path.isfile(dest_or_file):
        with open(dest_or_file) as f:
            ping_result_text = f.read()
    else:
        transmitter = PingTransmitter()
        transmitter.destination = dest_or_file
        transmitter.interface = interface
        transmitter.count = count
        transmitter.packet_size = packet_size
        transmitter.ttl = ttl
        transmitter.deadline = deadline
        transmitter.timeout = timeout
        transmitter.is_quiet = not is_parse_icmp_reply
        transmitter.timestamp = timestamp != TimestampFormat.NONE
        transmitter.ping_option = addopts

        try:
            result = transmitter.ping()
        except CommandError as e:
            logger.error(e)
            sys.exit(e.errno)

        ping_result_text = result.stdout
        if result.returncode != 0:
            if result.stderr:
                logger.error(result.stderr)

    if timezone_name:
        ping_parser = PingParsing(timezone=timezone(timezone_name))
    else:
        ping_parser = PingParsing()

    stats = ping_parser.parse(ping_result_text)
    output = stats.as_dict(include_icmp_replies=is_parse_icmp_reply)

    return (dest_or_file, output)


def get_ping_param(options) -> Tuple:
    count = options.count
    deadline = options.deadline
    timeout = options.timeout

    if not options.count and not options.deadline:
        count = DEFAULT_COUNT

    return (count, deadline, timeout)


def print_result(text: str, colorize: bool) -> None:
    if not sys.stdout.isatty() or not colorize:
        # avoid to colorized when piped or redirected
        print(text)
        return

    try:
        from pygments import highlight
        from pygments.formatters import TerminalTrueColorFormatter
        from pygments.lexers import JsonLexer

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

    raise TypeError(f"not supported type to convert: {type(obj)}")


def _serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, TIMESTAMP_TYPES):
        return obj

    raise TypeError(f"not supported type to convert: {type(obj)}")


timestamp_serialize_map = {
    TimestampFormat.NONE: _serialize_datetime,
    TimestampFormat.EPOCH: _serialize_epoch,
    TimestampFormat.DATETIME: _serialize_datetime,
}


def dumps_dict(obj: Dict, timestamp_format: str, indent: int = 0) -> str:
    serialize_func = timestamp_serialize_map[timestamp_format]

    if indent <= 0:
        return json.dumps(obj, default=serialize_func)

    return json.dumps(obj, indent=indent, default=serialize_func)


def main() -> int:
    options = parse_option()

    initialize_logger(options.log_level)

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
                    future_list.append(
                        executor.submit(
                            parse_ping,
                            dest_or_file,
                            options.interface,
                            count,
                            options.packet_size,
                            options.ttl,
                            deadline,
                            timeout,
                            options.icmp_reply,
                            options.timestamp,
                            options.timezone,
                            options.addopts if options.addopts is not None else [],
                        )
                    )

                for future in futures.as_completed(future_list):
                    key, ping_data = future.result()
                    output[key] = ping_data
        finally:
            executor.shutdown()
    else:
        ping_result_text = sys.stdin.read()
        ping_parser = PingParsing()
        stats = ping_parser.parse(ping_result_text)
        output = stats.as_dict(include_icmp_replies=options.icmp_reply)

    print_result(
        dumps_dict(output, timestamp_format=options.timestamp, indent=options.indent),
        colorize=not options.no_color,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
