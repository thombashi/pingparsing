"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from datetime import tzinfo
from typing import Optional, Union

import pyparsing as pp
import typepy

from ._common import _to_unicode
from ._logger import logger
from ._parser import PingParser  # noqa
from ._parser import (
    AlpineLinuxPingParser,
    LinuxPingParser,
    MacOsPingParser,
    NullPingParser,
    WindowsPingParser,
)
from ._pingtransmitter import PingResult
from ._stats import PingStats
from .error import ParseError, ParseErrorReason


class PingParsing:
    """
    Parser class to parsing ping command output.

    Args:
        timezone (Optional[tzinfo]):
            Time zone for parsing timestamps.
    """

    def __init__(self, timezone: Optional[tzinfo] = None) -> None:
        self.__parser: PingParser = NullPingParser()
        self.__timezone = timezone

    @property
    def parser_name(self) -> str:
        return self.__parser._parser_name

    def parse(self, ping_message: Union[str, PingResult]) -> PingStats:
        """
        Parse ping command output.

        Args:
            ping_message (str or :py:class:`~pingparsing.PingResult`):
                ``ping`` command output.

        Returns:
            :py:class:`~pingparsing.PingStats`: Parsed result.
        """

        if isinstance(ping_message, PingResult):
            # accept PingResult instance as an input
            if typepy.is_not_null_string(ping_message.stdout):
                ping_text = ping_message.stdout
            else:
                ping_text = ""
        else:
            ping_text = ping_message

        logger.debug(f"parsing ping result: {ping_text}")

        self.__parser = NullPingParser()

        if typepy.is_null_string(ping_text):
            logger.debug("ping_message is empty")

            return PingStats()

        ping_lines = _to_unicode(ping_text).splitlines()
        parser_class_list = (
            LinuxPingParser,
            WindowsPingParser,
            MacOsPingParser,
            AlpineLinuxPingParser,
        )

        for parser_class in parser_class_list:
            self.__parser = parser_class(timezone=self.__timezone)  # type: ignore
            try:
                return self.__parser.parse(ping_lines)
            except ParseError as e:
                if e.reason != ParseErrorReason.HEADER_NOT_FOUND:
                    raise e
            except pp.ParseException:
                pass

        self.__parser = NullPingParser()

        return PingStats()
