"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from collections import namedtuple

import pytest

from pingparsing import PingParsing


@pytest.fixture
def ping_parser():
    return PingParsing()


PingTestData = namedtuple("PingTestData", "value expected replies")
