"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from collections import namedtuple

import pytest
import pytz

from pingparsing import PingParsing


@pytest.fixture
def ping_parser():
    return PingParsing(timezone=pytz.UTC)


PingTestData = namedtuple("PingTestData", "value expected replies")
