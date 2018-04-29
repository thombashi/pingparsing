**pingparsing**

.. contents:: Table of Contents
   :depth: 2

Summary
=========
pingparsing is a CLI-tool/Python-library for parsing ping command output.

.. image:: https://badge.fury.io/py/pingparsing.svg
    :target: https://badge.fury.io/py/pingparsing

.. image:: https://img.shields.io/travis/thombashi/pingparsing/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/pingparsing

.. image:: https://img.shields.io/appveyor/ci/thombashi/pingparsing/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pingparsing

.. image:: https://img.shields.io/github/stars/thombashi/pingparsing.svg?style=social&label=Star
   :target: https://github.com/thombashi/pingparsing

CLI Usage
====================
CLI included in the ``pingparsing`` packaged. The ``pingparsing`` command could do the followings:

- Execute ping and parse the result
- Parse ping result file(s)
- Parse from the standard input

Execute ping and parse the result
--------------------------------------------
If you specify destination(s) to the ``pingparsing`` command as positional arguments,
the command executes ping for each destination(s) and parses the result.
The parsed result output with JSON format.

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
            "rtt_min": 136.097,
            "rtt_avg": 140.476,
            "rtt_max": 148.341,
            "rtt_mdev": 5.589,
            "packet_duplicate_count": 0,
            "packet_duplicate_rate": 0.0,
            "icmp_reply": [
                {
                    "timestamp": null,
                    "icmp_seq": 1,
                    "ttl": 39,
                    "time": 148.0,
                    "duplicate": false
                },
                {
                    "timestamp": null,
                    "icmp_seq": 2,
                    "ttl": 39,
                    "time": 136.0,
                    "duplicate": false
                },
                {
                    "timestamp": null,
                    "icmp_seq": 3,
                    "ttl": 39,
                    "time": 136.0,
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
                "icmp_reply": []
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
                "icmp_reply": [
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

    $ ping -f -w 10 192.168.2.100 | pingparsing
    {
        "destination": "192.168.2.100",
        "packet_transmit": 1302,
        "packet_receive": 1156,
        "packet_loss_rate": 11.213517665130567,
        "packet_loss_count": 146,
        "rtt_min": 0.142,
        "rtt_avg": 44.569,
        "rtt_max": 314.637,
        "rtt_mdev": 60.714,
        "packet_duplicate_rate": 5.190311418685121,
        "packet_duplicate_count": 60
    }

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
        transmitter.destination_host = "google.com"
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

        print("[ping statistics]")
        print(json.dumps(stats.as_dict(), indent=4))

        print("\n[icmp reply]")
        for icmp_reply in stats.icmp_reply_list:
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

        [icmp reply]
        {'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 37), 'icmp_seq': 1, 'ttl': 39, 'time': 148.0, 'duplicate': False}
        {'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 37), 'icmp_seq': 2, 'ttl': 39, 'time': 137.0, 'duplicate': False}
        {'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 38), 'icmp_seq': 3, 'ttl': 39, 'time': 137.0, 'duplicate': False}
        {'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 39), 'icmp_seq': 4, 'ttl': 39, 'time': 136.0, 'duplicate': False}
        {'timestamp': datetime.datetime(2018, 4, 29, 0, 55, 40), 'icmp_seq': 5, 'ttl': 39, 'time': 136.0, 'duplicate': False}


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
Python 2.7+ or 3.4+

- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `pyparsing <https://pyparsing.wikispaces.com/>`__
- `six <https://pypi.python.org/pypi/six/>`__
- `subprocrunner <https://github.com/thombashi/subprocrunner>`__
- `typepy <https://github.com/thombashi/typepy>`__

Test dependencies
-----------------
- `pytest <https://pypi.python.org/pypi/pytest>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://pypi.python.org/pypi/tox>`__


Tested Environment
==================

+--------------+-----------------------------------+
| OS           | ping version                      |
+==============+===================================+
| Debian 8.6   | ``iputils-ping 20121221-5+b2``    |
+--------------+-----------------------------------+
| Ubuntu 16.04 | ``iputils-ping 20121221-5ubuntu2``|
+--------------+-----------------------------------+
| Fedora 25    | ``iputils-20161105-1.fc25.x86_64``|
+--------------+-----------------------------------+
| Windows 10   | ``-``                             |
+--------------+-----------------------------------+
| macOS 10.13  | ``-``                             |
+--------------+-----------------------------------+

Supported Environment
============================
- Linux
- Windows
- macOS

Premise
=======
``pingparsing`` expects the locale at the ping command execution environment with English.
Parsing the ``ping`` command output with any other locale may fail.
This is because the output of the ``ping`` command will change depending on the locale setting.

Documentation
===============
http://pingparsing.rtfd.io/

