"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from pingparsing import *


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingTransmitter_ping:

    @pytest.mark.xfail
    @pytest.mark.parametrize(["host", "waittime", "expected"], [
        ["localhost", 3, ValueError],
    ])
    def test_normal(self, transmitter, host, waittime, expected):
        transmitter.destination_host = host
        transmitter.waittime = waittime
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
    def test_except(self,  transmitter, host, waittime, expected):
        transmitter.destination_host = host
        transmitter.waittime = waittime
        with pytest.raises(expected):
            transmitter.ping()
