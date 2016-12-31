# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class PingStaticticsHeaderNotFoundError(Exception):
    """
    Exception raised when a ping statistics header is not found in
    a parsing text.
    """


class EmptyPingStaticticsError(Exception):
    """
    Exception raised when a ping statistics is empty in a parsing text.
    """
