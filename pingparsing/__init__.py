"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._logger import set_log_level, set_logger
from ._pingparsing import PingParsing
from ._pingtransmitter import PingResult, PingTransmitter
from ._stats import PingStats
from .error import ParseError


__all__ = (
    "set_log_level",
    "set_logger",
    "PingParsing",
    "PingResult",
    "PingStats",
    "PingTransmitter",
    "ParseError",
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__version__",
)
