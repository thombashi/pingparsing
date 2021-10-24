"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import json
import sys
from textwrap import dedent

import pytest
from subprocrunner import SubprocessRunner

from .data import DEBIAN_SUCCESS_0, UBUNTU_SUCCESS_1, UBUNTU_SUCCESS_2, WINDOWS7SP1_SUCCESS


def print_result(stdout, stderr, expected=None):
    if expected:
        print(f"[expected]\n{expected}")

    print(f"[stdout]\n{stdout}")
    print(f"[stderr]\n{stderr}")


@pytest.mark.xfail(run=False)
class Test_cli_file:
    def test_normal_single(self, tmpdir):
        tmp_ping_file = tmpdir.join("ping_deb.txt")
        tmp_ping_file.write(DEBIAN_SUCCESS_0.value)
        tmp_ping_path = str(tmp_ping_file)

        runner = SubprocessRunner([sys.executable, "-m", "pingparsing", tmp_ping_path])
        runner.run()
        print_result(stdout=runner.stdout, stderr=runner.stderr)
        assert runner.returncode == 0
        assert json.loads(runner.stdout)[tmp_ping_path] == DEBIAN_SUCCESS_0.expected

        runner = SubprocessRunner(
            [sys.executable, "-m", "pingparsing", tmp_ping_path, "--no-color"]
        )
        runner.run()
        print_result(stdout=runner.stdout, stderr=runner.stderr)
        assert runner.returncode == 0
        assert json.loads(runner.stdout)[tmp_ping_path] == DEBIAN_SUCCESS_0.expected

    def test_normal_multi(self, tmpdir):
        tmp_ping_file_deb = tmpdir.join("ping_deb.txt")
        tmp_ping_file_deb.write(DEBIAN_SUCCESS_0.value)
        tmp_ping_path_deb = str(tmp_ping_file_deb)

        tmp_ping_file_win = tmpdir.join("ping_win.txt")
        tmp_ping_file_win.write(WINDOWS7SP1_SUCCESS.value)
        tmp_ping_path_win = str(tmp_ping_file_win)

        runner = SubprocessRunner(
            [sys.executable, "-m", "pingparsing", tmp_ping_path_deb, tmp_ping_path_win]
        )
        runner.run()

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)
        assert parsed_result[tmp_ping_path_deb] == DEBIAN_SUCCESS_0.expected
        assert parsed_result[tmp_ping_path_win] == WINDOWS7SP1_SUCCESS.expected

    def test_normal_timezone(self, tmpdir):
        tmp_ping_file = tmpdir.join("ping_timezone.txt")
        tmp_ping_file.write(UBUNTU_SUCCESS_1.value)
        tmp_ping_path = str(tmp_ping_file)

        runner = SubprocessRunner(
            [
                sys.executable,
                "-m",
                "pingparsing",
                "--icmp-reply",
                "--timezone",
                "UTC",
                "--no-color",
                tmp_ping_path,
            ]
        )
        runner.run()
        print_result(stdout=runner.stdout, stderr=runner.stderr)
        assert runner.returncode == 0
        assert json.loads(runner.stdout)[tmp_ping_path] == {
            "destination": "google.com",
            "packet_transmit": 5,
            "packet_receive": 5,
            "packet_loss_count": 0,
            "packet_loss_rate": 0.0,
            "rtt_min": 136.537,
            "rtt_avg": 139.174,
            "rtt_max": 148.006,
            "rtt_mdev": 4.425,
            "packet_duplicate_count": 0,
            "packet_duplicate_rate": 0.0,
            "icmp_replies": [
                {
                    "destination": "74.125.24.100",
                    "bytes": 64,
                    "timestamp": "2018-04-28T15:55:37.003555+00:00",
                    "icmp_seq": 1,
                    "ttl": 39,
                    "time": 148.0,
                    "duplicate": False,
                },
                {
                    "destination": "74.125.24.100",
                    "bytes": 64,
                    "timestamp": "2018-04-28T15:55:37.787175+00:00",
                    "icmp_seq": 2,
                    "ttl": 39,
                    "time": 137.0,
                    "duplicate": False,
                },
                {
                    "destination": "74.125.24.100",
                    "bytes": 64,
                    "timestamp": "2018-04-28T15:55:38.787642+00:00",
                    "icmp_seq": 3,
                    "ttl": 39,
                    "time": 137.0,
                    "duplicate": False,
                },
                {
                    "destination": "74.125.24.100",
                    "bytes": 64,
                    "timestamp": "2018-04-28T15:55:39.787653+00:00",
                    "icmp_seq": 4,
                    "ttl": 39,
                    "time": 136.0,
                    "duplicate": False,
                },
                {
                    "destination": "74.125.24.100",
                    "bytes": 64,
                    "timestamp": "2018-04-28T15:55:40.788365+00:00",
                    "icmp_seq": 5,
                    "ttl": 39,
                    "time": 136.0,
                    "duplicate": False,
                },
            ],
        }


@pytest.mark.xfail(run=False)
class Test_cli_pipe:
    def test_normal(self):
        runner = SubprocessRunner([sys.executable, "-m", "pingparsing"])
        runner.run(input=DEBIAN_SUCCESS_0.value)

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0
        assert json.loads(runner.stdout) == DEBIAN_SUCCESS_0.expected

    def test_normal_w_option(self):
        expected = dedent(
            """\
            {
                "destination": "google.com",
                "packet_transmit": 3,
                "packet_receive": 3,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "rtt_min": 48.832,
                "rtt_avg": 54.309,
                "rtt_max": 64.334,
                "rtt_mdev": 7.098,
                "packet_duplicate_count": 0,
                "packet_duplicate_rate": 0.0,
                "icmp_replies": [
                    {
                        "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
                        "bytes": 64,
                        "icmp_seq": 1,
                        "ttl": 50,
                        "time": 64.3,
                        "duplicate": false
                    },
                    {
                        "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
                        "bytes": 64,
                        "icmp_seq": 2,
                        "ttl": 50,
                        "time": 49.7,
                        "duplicate": false
                    },
                    {
                        "destination": "kix05s01-in-f14.1e100.net (172.217.26.110)",
                        "bytes": 64,
                        "icmp_seq": 3,
                        "ttl": 50,
                        "time": 48.8,
                        "duplicate": false
                    }
                ]
            }
            """
        )
        runner = SubprocessRunner([sys.executable, "-m", "pingparsing", "-", "--icmp-reply"])
        runner.run(input=UBUNTU_SUCCESS_2.value)

        print_result(stdout=runner.stdout, stderr=runner.stderr, expected=expected)

        assert runner.returncode == 0
        assert json.loads(runner.stdout) == json.loads(expected)


@pytest.mark.xfail(run=False)
class Test_PingParsing_ping:
    def test_normal_single(self):
        count = 1
        dest = "localhost"
        runner = SubprocessRunner([sys.executable, "-m", "pingparsing", dest, "-c", count])
        runner.run()

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)

        assert parsed_result[dest]["packet_transmit"] == count
        assert parsed_result[dest]["rtt_max"] > 0

    def test_normal_multi(self):
        count = 1
        dest_list = ["google.com", "twitter.com"]
        runner = SubprocessRunner([sys.executable, "-m", "pingparsing"] + dest_list + ["-c", count])
        print(runner.command_str, file=sys.stderr)
        runner.run()

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)
        for dest in dest_list:
            assert parsed_result[dest]["packet_transmit"] == count
            assert parsed_result[dest]["rtt_max"] > 0

    def test_normal_single_icmp_timestamp(self):
        count = 1
        dest = "localhost"
        runner = SubprocessRunner(
            [
                sys.executable,
                "-m",
                "pingparsing",
                dest,
                "-c",
                count,
                "--icmp-reply",
                "--timestamp",
                "epoch",
            ]
        )
        runner.run()

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)

        assert parsed_result[dest]["packet_transmit"] == count
        assert parsed_result[dest]["rtt_max"] > 0

        icmp_replies = parsed_result[dest]["icmp_replies"]
        assert icmp_replies
        assert icmp_replies[0]["timestamp"]
