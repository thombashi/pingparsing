"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
from typepy import RealNumber

from pingparsing import PingTransmitter
from pingparsing._parser import IcmpReplyKey

from .common import ping_parser  # noqa: W0611


@pytest.fixture
def transmitter():
    return PingTransmitter()


class Test_PingTransmitter_ping:
    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host"], [["localhost"], ["127.0.0.1"], ["::1"]])
    def test_normal_dest(self, transmitter, host):
        transmitter.destination = host
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "deadline"], [["localhost", 1]])
    def test_normal_deadline(self, transmitter, host, deadline):
        transmitter.destination = host
        transmitter.deadline = deadline
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "timeout"], [["localhost", 1]])
    def test_normal_timeout(self, transmitter, host, timeout):
        transmitter.destination = host
        transmitter.timeout = timeout
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(
        ["host", "count", "deadline"], [["localhost", 1, None], ["localhost", 1, 1000]]
    )
    def test_normal_count(self, transmitter, host, count, deadline):
        transmitter.destination = host
        transmitter.deadline = deadline
        transmitter.count = count
        result = transmitter.ping()

        assert result.returncode == 0
        assert len(result.stdout) > 0

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "count"], [["localhost", 3]])
    def test_normal_send_parse(self, transmitter, ping_parser, host, count):
        transmitter.destination = host
        transmitter.count = count
        result = transmitter.ping()

        stats = ping_parser.parse(result.stdout)

        assert stats.packet_transmit >= count
        assert RealNumber(stats.packet_receive).is_type()
        assert RealNumber(stats.packet_loss_rate).is_type()
        assert RealNumber(stats.packet_loss_count).is_type()
        assert RealNumber(stats.packet_duplicate_rate).is_type()
        assert RealNumber(stats.packet_duplicate_count).is_type()
        assert RealNumber(stats.rtt_min).is_type()
        assert RealNumber(stats.rtt_avg).is_type()
        assert RealNumber(stats.rtt_max).is_type()
        assert RealNumber(stats.rtt_mdev).is_type()
        assert IcmpReplyKey.TIMESTAMP not in stats.icmp_replies[0]

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(["host", "count"], [["localhost", 3]])
    def test_normal_send_parse_timestamp(self, transmitter, ping_parser, host, count):
        transmitter.destination = host
        transmitter.count = count
        transmitter.timestamp = True
        result = transmitter.ping()

        stats = ping_parser.parse(result.stdout)

        assert stats.packet_transmit >= count
        assert RealNumber(stats.packet_receive).is_type()
        assert RealNumber(stats.packet_loss_rate).is_type()
        assert RealNumber(stats.packet_loss_count).is_type()
        assert RealNumber(stats.packet_duplicate_rate).is_type()
        assert RealNumber(stats.packet_duplicate_count).is_type()
        assert RealNumber(stats.rtt_min).is_type()
        assert RealNumber(stats.rtt_avg).is_type()
        assert RealNumber(stats.rtt_max).is_type()
        assert RealNumber(stats.rtt_mdev).is_type()
        assert IcmpReplyKey.TIMESTAMP in stats.icmp_replies[0]

    @pytest.mark.parametrize(
        ["dest", "expected"], [["", ValueError], [None, ValueError], [1, ValueError]]
    )
    def test_except_destination(self, transmitter, dest, expected):
        with pytest.raises(expected):
            transmitter.destination = dest

    @pytest.mark.parametrize(
        ["host", "deadline", "expected"],
        [
            ["localhost", 0, ValueError],
            ["localhost", -1, ValueError],
            ["localhost", "a", ValueError],
        ],
    )
    def test_except_deadline(self, transmitter, host, deadline, expected):
        transmitter.destination = host

        with pytest.raises(expected):
            transmitter.deadline = deadline
            transmitter.ping()

    @pytest.mark.parametrize(
        ["host", "timeout", "expected"],
        [
            ["localhost", 0, ValueError],
            ["localhost", -1, ValueError],
            ["localhost", "a", ValueError],
        ],
    )
    def test_except_timeout(self, transmitter, host, timeout, expected):
        transmitter.destination = host

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
        transmitter.destination = host
        transmitter.count = count
        with pytest.raises(expected):
            transmitter.ping()
