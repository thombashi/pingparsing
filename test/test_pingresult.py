# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import pytest
from pingparsing import PingResult

from .common import ping_parser  # noqa: W0611
from .data import DEBIAN_SUCCESS_0


class Test_PingResult(object):
    @pytest.mark.parametrize(
        ["pingresult", "expected"],
        [[PingResult(DEBIAN_SUCCESS_0.value, "", 0), DEBIAN_SUCCESS_0.expected]],
    )
    def test_normal_pingresult(self, ping_parser, pingresult, expected):
        ping_parser.parse(pingresult.stdout)
        assert ping_parser.as_dict() == expected

        ping_parser.parse(pingresult)
        assert ping_parser.as_dict() == expected
