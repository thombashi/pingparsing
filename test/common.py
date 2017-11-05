# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from collections import namedtuple

from pingparsing import PingParsing
import pytest


@pytest.fixture
def ping_parser():
    return PingParsing()


PingTestData = namedtuple("PingTestData", "value expected")
