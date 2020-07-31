"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import json
import sys
from textwrap import dedent

import pytest
from subprocrunner import SubprocessRunner

from .data import DEBIAN_SUCCESS_0, UBUNTU_SUCCESS_2, WINDOWS7SP1_SUCCESS


def print_result(stdout, stderr, expected=None):
    if expected:
        print("[expected]\n{}".format(expected))

    print("[stdout]\n{}".format(stdout))
    print("[stderr]\n{}".format(stderr))


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


@pytest.mark.xfail(run=False)
class Test_cli_pipe:
    def test_normal(self, tmpdir):
        runner = SubprocessRunner([sys.executable, "-m", "pingparsing"])
        runner.run(input=DEBIAN_SUCCESS_0.value)

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert runner.returncode == 0
        assert json.loads(runner.stdout) == DEBIAN_SUCCESS_0.expected

    def test_normal_w_option(self, tmpdir):
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
                        "icmp_seq": 1,
                        "ttl": 50,
                        "time": 64.3,
                        "duplicate": false
                    },
                    {
                        "icmp_seq": 2,
                        "ttl": 50,
                        "time": 49.7,
                        "duplicate": false
                    },
                    {
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
