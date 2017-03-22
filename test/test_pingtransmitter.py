# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from pingparsing import PingTransmitter
import pytest


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingTransmitter_ping:

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "waittime"], [
        ["localhost", 3],
    ])
    def test_normal_waittime(self, transmitter, host, waittime):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "count", "waittime"], [
        ["localhost", 1, None],
        ["localhost", 1, 1000],
    ])
    def test_normal_count(self, transmitter, host, count, waittime):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        transmitter.count = count
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["", 1, ValueError],
        ["localhost", 0, ValueError],
        ["localhost", -1, ValueError],
        ["localhost", "a", ValueError],
        [None, 1, ValueError],
    ])
    def test_except_waittime(self,  transmitter, host, waittime, expected):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        with pytest.raises(expected):
            transmitter.ping()

    @pytest.mark.parametrize(["host", "count", "expected"], [
        ["localhost", 0, ValueError],
        ["localhost", -1, ValueError],
        ["localhost", "a", ValueError],
    ])
    def test_except_count(self,  transmitter, host, count, expected):
        transmitter.destination_host = host
        transmitter.count = count
        with pytest.raises(expected):
            transmitter.ping()
