# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import enum


@enum.unique
class ParseErrorReason(enum.Enum):
    HEADER_NOT_FOUND = "ping statistics not found"
    EMPTY_STATISTICS = "ping statistics is empty"


class ParseError(Exception):
    """
    Exception raised when failed to parse ping results.
    """

    @property
    def reason(self):
        return self.__reason

    def __init__(self, *args, **kwargs):
        self.__reason = kwargs.pop("reason", None)

        super(ParseError, self).__init__(*args, **kwargs)
