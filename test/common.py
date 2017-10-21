# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from pingparsing import PingParsing
import pytest


@pytest.fixture
def ping_parser():
    return PingParsing()
