"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from pingparsing import PingResult

from .common import ping_parser  # noqa: W0611
from .data import DEBIAN_SUCCESS_0


class Test_PingResult:
    @pytest.mark.parametrize(
        ["pingresult", "expected"],
        [[PingResult(DEBIAN_SUCCESS_0.value, "", 0), DEBIAN_SUCCESS_0.expected]],
    )
    def test_normal_pingresult(self, ping_parser, pingresult, expected):
        assert ping_parser.parse(pingresult.stdout).as_dict() == expected
        assert ping_parser.parse(pingresult).as_dict() == expected
