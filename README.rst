.. contents:: **pingparsing**
   :backlinks: top
   :depth: 2

Summary
=========
`pingparsing <https://github.com/thombashi/pingparsing>`__ is a CLI-tool/Python-library parser and transmitter for ping command.

.. image:: https://badge.fury.io/py/pingparsing.svg
    :target: https://badge.fury.io/py/pingparsing
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/pingparsing.svg
    :target: https://pypi.org/project/pingparsing
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/pingparsing.svg
    :target: https://pypi.org/project/pingparsing
    :alt: Supported Python implementations

.. image:: https://github.com/thombashi/pingparsing/workflows/Tests/badge.svg
    :target: https://github.com/thombashi/pingparsing/actions?query=workflow%3ATests
    :alt: Linux/macOS/Windows CI status

.. image:: https://github.com/thombashi/pingparsing/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/thombashi/pingparsing/actions/workflows/codeql-analysis.yml
    :alt: CodeQL

CLI Usage
====================
A CLI command (``pingparsing`` command) is included in the package. The command could do the following:

- Execute ``ping`` and parse the result
- Parse ping results from:
    - file(s)
    - the standard input

Execute ping and parse the result
--------------------------------------------
If you specify destination(s) to the ``pingparsing`` command as positional arguments,
the command executes ``ping`` for each destination(s) and parses the result.
``ping`` will execute in parallel for multiple destinations.
The parsed result is outputted in JSON format.

.. code-block:: console

    $ pingparsing google.com
    {
        "google.com": {
            "destination": "google.com",
            "packet_transmit": 10,
            "packet_receive": 10,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 34.189,
            "rtt_avg": 46.054,
            "rtt_max": 63.246,
            "rtt_mdev": 9.122,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0
        }
    }

.. code-block:: console

    $ pingparsing google.com twitter.com
    {
        "google.com": {
            "destination": "google.com",
            "packet_transmit": 10,
            "packet_receive": 10,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 37.341,
            "rtt_avg": 44.538,
            "rtt_max": 53.997,
            "rtt_mdev": 5.827,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0
        },
        "twitter.com": {
            "destination": "twitter.com",
            "packet_transmit": 10,
            "packet_receive": 10,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 45.377,
            "rtt_avg": 68.819,
            "rtt_max": 78.581,
            "rtt_mdev": 9.769,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0
        }
    }

.. code-block:: console

    $ pingparsing google.com -c 3 --icmp-reply
    {
        "google.com": {
            "destination": "google.com",
            "packet_transmit": 3,
            "packet_receive": 3,
            "packet_loss_count": 0,
            "packet_loss_rate": 0.0,
            "rtt_min": 36.997,
            "rtt_avg": 49.1,
            "rtt_max": 60.288,
            "rtt_mdev": 9.533,
            "packet_duplicate_count": 0,
            "packet_duplicate_rate": 0.0,
            "icmp_replies": [
                {
                    "destination": "nrt20s21-in-f14.1e100.net (172.217.175.110)",
                    "bytes": 64,
                    "icmp_seq": 1,
                    "ttl": 113,
                    "time": 50.0,
                    "duplicate": false
                },
                {
                    "destination": "nrt20s21-in-f14.1e100.net (172.217.175.110)",
                    "bytes": 64,
                    "icmp_seq": 2,
                    "ttl": 113,
                    "time": 60.2,
                    "duplicate": false
                },
                {
                    "destination": "nrt20s21-in-f14.1e100.net (172.217.175.110)",
                    "bytes": 64,
                    "icmp_seq": 3,
                    "ttl": 113,
                    "time": 36.9,
                    "duplicate": false
                }
            ]
        }
    }


Parse ping result file
--------------------------------------------
:Input:
    .. code-block:: console

        $ cat ping.txt
        PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.

        --- 192.168.0.1 ping statistics ---
        1688 packets transmitted, 1553 received, +1 duplicates, 7% packet loss, time 2987ms
        rtt min/avg/max/mdev = 0.282/0.642/11.699/0.699 ms, pipe 2, ipg/ewma 1.770/0.782 ms
        $ cat osx.txt
        PING google.com (172.217.6.238): 56 data bytes
        64 bytes from 172.217.6.238: icmp_seq=0 ttl=53 time=20.482 ms
        64 bytes from 172.217.6.238: icmp_seq=1 ttl=53 time=32.550 ms
        64 bytes from 172.217.6.238: icmp_seq=2 ttl=53 time=32.013 ms
        64 bytes from 172.217.6.238: icmp_seq=3 ttl=53 time=28.498 ms
        64 bytes from 172.217.6.238: icmp_seq=4 ttl=53 time=46.093 ms

        --- google.com ping statistics ---
        5 packets transmitted, 5 packets received, 0.0% packet loss
        round-trip min/avg/max/stddev = 20.482/31.927/46.093/8.292 ms

:Output:
    .. code-block:: console

        $ pingparsing ping.txt osx.txt
        {
            "osx.txt": {
                "destination": "google.com",
                "packet_transmit": 5,
                "packet_receive": 5,
                "packet_loss_rate": 0.0,
                "packet_loss_count": 0,
                "rtt_min": 20.482,
                "rtt_avg": 31.927,
                "rtt_max": 46.093,
                "rtt_mdev": 8.292,
                "packet_duplicate_rate": null,
                "packet_duplicate_count": null
            },
            "ping.txt": {
                "destination": "192.168.0.1",
                "packet_transmit": 1688,
                "packet_receive": 1553,
                "packet_loss_rate": 7.997630331753558,
                "packet_loss_count": 135,
                "rtt_min": 0.282,
                "rtt_avg": 0.642,
                "rtt_max": 11.699,
                "rtt_mdev": 0.699,
                "packet_duplicate_rate": 0.0643915003219575,
                "packet_duplicate_count": 1
            }
        }

    .. code-block:: console

        $ pingparsing ping.txt osx.txt --icmp-reply
        {
            "ping.txt": {
                "destination": "google.com",
                "packet_transmit": 60,
                "packet_receive": 60,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "rtt_min": 61.425,
                "rtt_avg": 99.731,
                "rtt_max": 212.597,
                "rtt_mdev": 27.566,
                "packet_duplicate_count": 0,
                "packet_duplicate_rate": 0.0,
                "icmp_replies": []
            },
            "osx.txt": {
                "destination": "google.com",
                "packet_transmit": 5,
                "packet_receive": 5,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "rtt_min": 20.482,
                "rtt_avg": 31.927,
                "rtt_max": 46.093,
                "rtt_mdev": 8.292,
                "packet_duplicate_count": 0,
                "packet_duplicate_rate": 0.0,
                "icmp_replies": [
                    {
                        "icmp_seq": 0,
                        "ttl": 53,
                        "time": 20.482,
                        "duplicate": false
                    },
                    {
                        "icmp_seq": 1,
                        "ttl": 53,
                        "time": 32.55,
                        "duplicate": false
                    },
                    {
                        "icmp_seq": 2,
                        "ttl": 53,
                        "time": 32.013,
                        "duplicate": false
                    },
                    {
                        "icmp_seq": 3,
                        "ttl": 53,
                        "time": 28.498,
                        "duplicate": false
                    },
                    {
                        "icmp_seq": 4,
                        "ttl": 53,
                        "time": 46.093,
                        "duplicate": false
                    }
                ]
            }
        }


Parse from the standard input
--------------------------------------------
.. code-block:: console

    $ ping -i 0.2 -w 20 192.168.2.101 | pingparsing -
    {
        "destination": "192.168.2.101",
        "packet_transmit": 99,
        "packet_receive": 88,
        "packet_loss_count": 11,
        "packet_loss_rate": 11.11111111111111,
        "rtt_min": 1.615,
        "rtt_avg": 26.581,
        "rtt_max": 93.989,
        "rtt_mdev": 19.886,
        "packet_duplicate_count": 0,
        "packet_duplicate_rate": 0.0
    }

CLI help
--------------------------------------------
::

    usage: pingparsing [-h] [-V] [--max-workers MAX_WORKERS]
                       [--timestamp {none,epoch,datetime}] [-c COUNT]
                       [-s PACKET_SIZE] [--ttl TTL] [-w DEADLINE]
                       [--timeout TIMEOUT] [-I INTERFACE] [--addopts OPTIONS]
                       [--indent INDENT] [--icmp-reply] [--timezone TIMEZONE]
                       [--no-color] [--debug | --quiet]
                       destination_or_file [destination_or_file ...]

    positional arguments:
      destination_or_file   Destinations to send ping or files to parse. '-' for
                            parsing the standard input.

    options:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      --max-workers MAX_WORKERS
                            Number of threads for when multiple destinations/files
                            are specified. Defaults to equal two times the number
                            of cores.
      --debug               for debug print.
      --quiet               suppress execution log messages.

    Ping Options:
      --timestamp {none,epoch,datetime}
                            [Only for LINUX] none: no timestamps. epoch: add
                            timestamps with UNIX epoch time format. datetime: add
                            timestamps with ISO time format.
      -c COUNT, --count COUNT
                            Stop after sending the count. see also ping(8) [-c
                            count] option description.
      -s PACKET_SIZE, --packet-size PACKET_SIZE
                            Specifies the number of data bytes to be sent.
      --ttl TTL             Specifies the Time to Live.
      -w DEADLINE, --deadline DEADLINE
                            Timeout before ping exits. valid time units are:
                            d/day/days, h/hour/hours, m/min/mins/minute/minutes,
                            s/sec/secs/second/seconds,
                            ms/msec/msecs/millisecond/milliseconds,
                            us/usec/usecs/microsecond/microseconds. if no unit
                            string found, considered seconds as the time unit. see
                            also ping(8) [-w deadline] option description. note:
                            meaning of the 'deadline' may differ system from to
                            system.
      --timeout TIMEOUT     Time to wait for a response per packet. Valid time
                            units are: d/day/days, h/hour/hours,
                            m/min/mins/minute/minutes, s/sec/secs/second/seconds,
                            ms/msec/msecs/millisecond/milliseconds,
                            us/usec/usecs/microsecond/microseconds. If no unit
                            string is found, consider milliseconds as the time
                            unit. Attempt to send packets with milliseconds
                            granularity in default. If the system does not support
                            timeout in milliseconds, round up as seconds. Use
                            system default if not specified. This option will be
                            ignored if the system does not support timeout itself.
                            See also ping(8) [-W timeout] option description.
                            note: meaning of the 'timeout' may differ from system
                            to system.
      -I INTERFACE, --interface INTERFACE
                            network interface
      --addopts OPTIONS     extra command line options

    Output Options:
      --indent INDENT       JSON output will be pretty-printed with the indent
                            level. (default= 4)
      --icmp-reply, --icmp-replies
                            print results for each ICMP packet reply.
      --timezone TIMEZONE   Time zone for timestamps.
      --no-color            Turn off colors.

    Documentation: https://pingparsing.rtfd.io/
    Issue tracker: https://github.com/thombashi/pingparsing/issues

Library Usage
====================

Execute ping and parse the result
--------------------------------------------
``PingTransmitter`` class can execute ``ping`` command and obtain the
ping output as a string.

:Sample Code:
    .. code-block:: python

        import json
        import pingparsing

        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = "google.com"
        transmitter.count = 10
        result = transmitter.ping()

        print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))

:Output:
    .. code-block:: json

        {
            "destination": "google.com",
            "packet_transmit": 10,
            "packet_receive": 10,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 34.458,
            "rtt_avg": 51.062,
            "rtt_max": 62.943,
            "rtt_mdev": 8.678,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0
        }


Parsing ``ping`` command output
-------------------------------
:Sample Code:
    .. code-block:: python

        import json
        from textwrap import dedent
        import pingparsing

        parser = pingparsing.PingParsing()
        stats = parser.parse(dedent("""\
            PING google.com (74.125.24.100) 56(84) bytes of data.
            [1524930937.003555] 64 bytes from 74.125.24.100: icmp_seq=1 ttl=39 time=148 ms
            [1524930937.787175] 64 bytes from 74.125.24.100: icmp_seq=2 ttl=39 time=137 ms
            [1524930938.787642] 64 bytes from 74.125.24.100: icmp_seq=3 ttl=39 time=137 ms
            [1524930939.787653] 64 bytes from 74.125.24.100: icmp_seq=4 ttl=39 time=136 ms
            [1524930940.788365] 64 bytes from 74.125.24.100: icmp_seq=5 ttl=39 time=136 ms

            --- google.com ping statistics ---
            5 packets transmitted, 5 received, 0% packet loss, time 4001ms
            rtt min/avg/max/mdev = 136.537/139.174/148.006/4.425 ms
            """))

        print("[extract ping statistics]")
        print(json.dumps(stats.as_dict(), indent=4))

        print("\n[extract icmp replies]")
        for icmp_reply in stats.icmp_replies:
            print(icmp_reply)

:Output:
    ::

        [ping statistics]
        {
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
            "packet_duplicate_rate": 0.0
        }

        [icmp replies]
        {'destination': '74.125.24.100', 'bytes': 64, 'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 37, 3555), 'icmp_seq': 1, 'ttl': 39, 'time': 148.0, 'duplicate': False}
        {'destination': '74.125.24.100', 'bytes': 64, 'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 37, 787175), 'icmp_seq': 2, 'ttl': 39, 'time': 137.0, 'duplicate': False}
        {'destination': '74.125.24.100', 'bytes': 64, 'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 38, 787642), 'icmp_seq': 3, 'ttl': 39, 'time': 137.0, 'duplicate': False}
        {'destination': '74.125.24.100', 'bytes': 64, 'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 39, 787653), 'icmp_seq': 4, 'ttl': 39, 'time': 136.0, 'duplicate': False}
        {'destination': '74.125.24.100', 'bytes': 64, 'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 40, 788365), 'icmp_seq': 5, 'ttl': 39, 'time': 136.0, 'duplicate': False}


Recommended ping command execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following methods are recommended to execute ``ping`` command to get the output for parsing.
These commands include an operation that changes the locale setting to English temporarily.

Linux
^^^^^
.. code:: console

    LC_ALL=C ping <host or IP address> -w <seconds> [option] > <output.file>

Windows
^^^^^^^
.. code:: console

    > chcp
    Active code page: <XXX>    # get current code page

    > chcp 437    # change code page to english
    > ping <host or IP address> -n <ping count> > <output.file>
    > chcp <XXX>    # restore code page

-  Reference
    - https://technet.microsoft.com/en-us/library/cc733037

Installation
============
::

    pip install pingparsing


Dependencies
============
- Python 3.6+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pingparsing/network/dependencies>`__

Optional Dependencies
------------------------------------
- pingparsing[cli] extras
    - `loguru <https://github.com/Delgan/loguru>`__
        - Used for logging if the package installed
    - `Pygments <http://pygments.org/>`__
        - Syntax highlighting to ``pingparsing`` command output when installed


Docker Image
==================
`thombashi/pingparsing - Docker Hub <https://hub.docker.com/r/thombashi/pingparsing/>`__

Supported Environments
============================
- Linux
- Windows
- macOS

Tested Environments
---------------------------

+--------------+-----------------------------------+
| OS           | ping version                      |
+==============+===================================+
| Ubuntu 16.04 | ``iputils-ping 20121221-5ubuntu2``|
+--------------+-----------------------------------+
| Ubuntu 18.04 | ``iputils-ping 20161105-1ubuntu2``|
+--------------+-----------------------------------+
| Ubuntu 20.04 | ``iputils-ping 20190709-3``       |
+--------------+-----------------------------------+
| Debian 8.6   | ``iputils-ping 20121221-5+b2``    |
+--------------+-----------------------------------+
| Fedora 25    | ``iputils-20161105-1.fc25.x86_64``|
+--------------+-----------------------------------+
| Windows 10   | ``-``                             |
+--------------+-----------------------------------+
| macOS 10.13  | ``-``                             |
+--------------+-----------------------------------+

Premise
=======
``pingparsing`` expects the locale at the ping command execution environment with English.
Parsing the ``ping`` command output with any other locale may fail.
This is because the output of the ``ping`` command will change depending on the locale setting.

Documentation
===============
https://pingparsing.rtfd.io/

Sponsors
====================================
.. image:: https://avatars.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4
   :target: https://github.com/chasbecker
   :alt: Charles Becker (chasbecker)
.. image:: https://avatars.githubusercontent.com/u/46711571?s=48&u=57687c0e02d5d6e8eeaf9177f7b7af4c9f275eb5&v=4
   :target: https://github.com/Arturi0
   :alt: onetime: Arturi0
.. image:: https://avatars.githubusercontent.com/u/3658062?s=48&v=4
   :target: https://github.com/b4tman
   :alt: onetime: Dmitry Belyaev (b4tman)

`Become a sponsor <https://github.com/sponsors/thombashi>`__

