# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from pingparsing import PingResult
import pytest

from .common import ping_parser
from .data import (
    DEBIAN_SUCCESS,
)


class Test_PingResult(object):

    @pytest.mark.parametrize(["pingresult", "expected"], [
        [
            PingResult(DEBIAN_SUCCESS.value, "", 0),
            DEBIAN_SUCCESS.expected
        ]
    ])
    def test_normal_pingresult(self, ping_parser, pingresult, expected):
        ping_parser.parse(pingresult.stdout)
        assert ping_parser.as_dict() == expected

        ping_parser.parse(pingresult)
        assert ping_parser.as_dict() == expected
