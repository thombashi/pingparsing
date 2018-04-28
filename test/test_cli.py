
"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import json

import pytest
from subprocrunner import SubprocessRunner

from .data import DEBIAN_SUCCESS_0, WINDOWS7SP1_SUCCESS


@pytest.mark.xfail
class Test_cli_file(object):

    def test_normal_single(self, tmpdir):
        tmp_ping_file = tmpdir.join("ping_deb.txt")
        tmp_ping_file.write(DEBIAN_SUCCESS_0.value)
        tmp_ping_path = str(tmp_ping_file)

        runner = SubprocessRunner(
            "pingparsing {}".format(tmp_ping_path))
        runner.run()

        print("[stdout]\n{}".format(runner.stdout))
        print("[stderr]\n{}".format(runner.stderr))

        assert runner.returncode == 0
        assert json.loads(runner.stdout)[
            tmp_ping_path] == DEBIAN_SUCCESS_0.expected

    def test_normal_multi(self, tmpdir):
        tmp_ping_file_deb = tmpdir.join("ping_deb.txt")
        tmp_ping_file_deb.write(DEBIAN_SUCCESS_0.value)
        tmp_ping_path_deb = str(tmp_ping_file_deb)

        tmp_ping_file_win = tmpdir.join("ping_win.txt")
        tmp_ping_file_win.write(WINDOWS7SP1_SUCCESS.value)
        tmp_ping_path_win = str(tmp_ping_file_win)

        runner = SubprocessRunner(
            "pingparsing {} {}".format(tmp_ping_path_deb, tmp_ping_path_win))
        runner.run()

        print("[stdout]\n{}".format(runner.stdout))
        print("[stderr]\n{}".format(runner.stderr))

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)
        assert parsed_result[tmp_ping_path_deb] == DEBIAN_SUCCESS_0.expected
        assert parsed_result[tmp_ping_path_win] == WINDOWS7SP1_SUCCESS.expected


@pytest.mark.xfail
class Test_cli_pipe(object):

    def test_normal_single(self, tmpdir):
        runner = SubprocessRunner("pingparsing")
        runner.run(input=DEBIAN_SUCCESS_0.value)

        print("[stdout]\n{}".format(runner.stdout))
        print("[stderr]\n{}".format(runner.stderr))

        assert runner.returncode == 0
        assert json.loads(runner.stdout) == DEBIAN_SUCCESS_0.expected


@pytest.mark.xfail
class Test_PingParsing_ping(object):

    def test_normal_single(self):
        count = 1
        dest = "localhost"
        runner = SubprocessRunner(
            "pingparsing {:s} -c {:d}".format(dest, count))
        runner.run()

        print("[stdout]\n{}".format(runner.stdout))
        print("[stderr]\n{}".format(runner.stderr))

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)

        assert parsed_result[dest]["packet_transmit"] == count
        assert parsed_result[dest]["rtt_max"] > 0

    def test_normal_multi(self):
        count = 1
        dest_list = ["google.com", "twitter.com"]
        runner = SubprocessRunner(
            "pingparsing {:s} -c {:d}".format(" ".join(dest_list), count))
        runner.run()

        print("[stdout]\n{}".format(runner.stdout))
        print("[stderr]\n{}".format(runner.stderr))

        assert runner.returncode == 0

        parsed_result = json.loads(runner.stdout)
        for dest in dest_list:
            assert parsed_result[dest]["packet_transmit"] == count
            assert parsed_result[dest]["rtt_max"] > 0
