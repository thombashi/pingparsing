# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import division

import abc


class PingParserInterface(object):

    @abc.abstractproperty
    def packet_transmit(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def packet_receive(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def packet_loss_rate(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def packet_loss_count(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def rtt_min(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def rtt_avg(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def rtt_max(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def rtt_mdev(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def packet_duplicate_rate(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def packet_duplicate_count(self):  # pragma: no cover
        pass
