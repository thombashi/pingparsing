# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import platform as m_platform  # noqa: W0611

import pytest
from humanreadable import ParameterError
from pingparsing import PingTransmitter
from typepy import RealNumber

from .common import ping_parser  # noqa: W0611


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingTransmitter_ping(object):
    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host"], [["localhost"], ["127.0.0.1"], ["::1"]])
    def test_normal_dest(self, transmitter, host):
        transmitter.destination_host = host
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "deadline"], [["localhost", 1]])
    def test_normal_deadline(self, transmitter, host, deadline):
        transmitter.destination_host = host
        transmitter.deadline = deadline
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "timeout"], [["localhost", 1]])
    def test_normal_timeout(self, transmitter, host, timeout):
        transmitter.destination_host = host
        transmitter.timeout = timeout
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(
        ["host", "count", "deadline"], [["localhost", 1, None], ["localhost", 1, 1000]]
    )
    def test_normal_count(self, transmitter, host, count, deadline):
        transmitter.destination_host = host
        transmitter.deadline = deadline
        transmitter.count = count
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "count"], [["localhost", 3]])
    def test_normal_send_parse(self, transmitter, ping_parser, host, count):
        transmitter.destination_host = host
        transmitter.count = count
        result = transmitter.ping()

        ping_parser.parse(result.stdout)

        assert ping_parser.packet_transmit >= count
        assert RealNumber(ping_parser.packet_receive).is_type()
        assert RealNumber(ping_parser.packet_loss_rate).is_type()
        assert RealNumber(ping_parser.packet_loss_count).is_type()
        assert RealNumber(ping_parser.packet_duplicate_rate).is_type()
        assert RealNumber(ping_parser.packet_duplicate_count).is_type()
        assert RealNumber(ping_parser.rtt_min).is_type()
        assert RealNumber(ping_parser.rtt_avg).is_type()
        assert RealNumber(ping_parser.rtt_max).is_type()
        assert RealNumber(ping_parser.rtt_mdev).is_type()

    @pytest.mark.parametrize(
        ["system", "timeout", "expected"],
        [
            ["Linux", 1, "-W 1"],
            ["Linux", 1500, "-W 2"],
            ["Windows", 1, "-w 1"],
            ["Windows", 1500, "-w 1500"],
            ["macos", 1, ""],
            ["macos", 1500, ""],
        ],
    )
    def test_normal_get_timeout_option(self, monkeypatch, transmitter, system, timeout, expected):
        def platform_mock():
            return system

        monkeypatch.setattr(m_platform, "system", platform_mock)

        transmitter.timeout = timeout

        assert transmitter._PingTransmitter__get_timeout_option() == expected

    @pytest.mark.parametrize(
        ["host", "deadline", "expected"],
        [
            ["", 1, ValueError],
            ["localhost", 0, ParameterError],
            ["localhost", -1, ParameterError],
            ["localhost", "a", ParameterError],
            [None, 1, ValueError],
        ],
    )
    def test_except_deadline(self, transmitter, host, deadline, expected):
        transmitter.destination_host = host
        with pytest.raises(expected):
            transmitter.deadline = deadline
            transmitter.ping()

    @pytest.mark.parametrize(
        ["host", "timeout", "expected"],
        [
            ["", 1, ValueError],
            ["localhost", 0, ParameterError],
            ["localhost", -1, ParameterError],
            ["localhost", "a", ParameterError],
            [None, 1, ValueError],
        ],
    )
    def test_except_timeout(self, transmitter, host, timeout, expected):
        transmitter.destination_host = host
        with pytest.raises(expected):
            transmitter.timeout = timeout
            transmitter.ping()

    @pytest.mark.parametrize(
        ["host", "count", "expected"],
        [
            ["localhost", 0, ValueError],
            ["localhost", -1, ValueError],
            ["localhost", "a", ValueError],
        ],
    )
    def test_except_count(self, transmitter, host, count, expected):
        transmitter.destination_host = host
        transmitter.count = count
        with pytest.raises(expected):
            transmitter.ping()
