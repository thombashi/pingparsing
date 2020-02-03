"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pyparsing as pp
import typepy

from ._common import _to_unicode
from ._interface import PingParserInterface
from ._logger import logger
from ._parser import (
    AlpineLinuxPingParser,
    LinuxPingParser,
    MacOsPingParser,
    NullPingParser,
    WindowsPingParser,
)
from ._stats import PingStats
from .error import ParseError, ParseErrorReason


class PingParsing(PingParserInterface):
    """
    Parser class to parsing ping command output.
    """

    def __init__(self):
        self.__parser = NullPingParser()
        self.__stats = None

    @property
    def parser_name(self):
        return self.__parser._parser_name

    def parse(self, ping_message):
        """
        Parse ping command output.

        Args:
            ping_message (str or :py:class:`~pingparsing.PingResult`):
                ``ping`` command output.

        Returns:
            :py:class:`~pingparsing.PingStats`: Parsed result.
        """

        try:
            # accept PingResult instance as an input
            if typepy.is_not_null_string(ping_message.stdout):
                ping_message = ping_message.stdout
            else:
                ping_message = ""
        except AttributeError:
            pass

        logger.debug("parsing ping result: {}".format(ping_message))

        self.__parser = NullPingParser()

        if typepy.is_null_string(ping_message):
            logger.debug("ping_message is empty")
            self.__stats = PingStats()

            return self.__stats

        ping_lines = _to_unicode(ping_message).splitlines()
        parser_class_list = (
            LinuxPingParser,
            WindowsPingParser,
            MacOsPingParser,
            AlpineLinuxPingParser,
        )

        for parser_class in parser_class_list:
            self.__parser = parser_class()
            try:
                self.__stats = self.__parser.parse(ping_lines)
                return self.__stats
            except ParseError as e:
                if e.reason != ParseErrorReason.HEADER_NOT_FOUND:
                    raise e
            except pp.ParseException:
                pass

        self.__parser = NullPingParser()

        return self.__stats
