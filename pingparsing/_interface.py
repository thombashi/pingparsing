# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, division

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class PingParserInterface(object):
    @abc.abstractmethod
    def parse(self, ping_message):  # pragma: no cover
        pass
