pingparsing
===========

.. image:: https://badge.fury.io/py/pingparsing.svg
    :target: https://badge.fury.io/py/pingparsing

.. image:: https://img.shields.io/pypi/pyversions/pingparsing.svg
   :target: https://pypi.python.org/pypi/pingparsing

.. image:: https://img.shields.io/travis/thombashi/pingparsing/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/pingparsing

.. image:: https://img.shields.io/appveyor/ci/thombashi/pingparsing/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pingparsing

Summary
-------

pingparsing is a python library of parsing ping command output.

Usage
=====

Execute ping and parse
----------------------

``PingTransmitter`` class can execute ``ping`` command and obtain the
ping output as a string.

Sample code
~~~~~~~~~~~

https://github.com/thombashi/pingparsing/blob/master/examples/ping_sample.py

Sample output: Debian 8
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    ./ping_sample.py -d 192.168.0.1
    # returncode ---
    0

    # properties ---
    packet_transmit: 10 packets
    packet_receive: 10 packets
    packet_loss: 0.0 %
    rtt_min: 0.445
    rtt_avg: 1.069
    rtt_max: 4.854
    rtt_mdev: 1.312

    # asdict ---
    {
        "packet_loss": 0.0,
        "packet_receive": 10,
        "packet_transmit": 10,
        "rtt_min": 0.445,
        "rtt_max": 4.854,
        "rtt_mdev": 1.312,
        "rtt_avg": 1.069
    }

Example execution result: Windows 10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    >ping_sample.py -d google.com
    # returncode ---
    0

    # properties ---
    packet_transmit: 10 packets
    packet_receive: 10 packets
    packet_loss: 0.0 %
    rtt_min: 30.0
    rtt_avg: 37.0
    rtt_max: 58.0
    rtt_mdev: None

    # asdict ---
    {
        "rtt_avg": 37.0,
        "rtt_max": 58.0,
        "packet_loss": 0.0,
        "packet_transmit": 10,
        "rtt_min": 30.0,
        "rtt_mdev": null,
        "packet_receive": 10
    }

Note: ``rtt_mdev`` not available with Windows


Parsing ``ping`` command output
-------------------------------

Sample code
~~~~~~~~~~~
https://github.com/thombashi/pingparsing/blob/master/examples/parse_sample.py


Example: Debian 8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Input
^^^^^

::

    # LC_ALL=C ping google.com -q -c 60 > ping.txt
    # cat ping.txt
    PING google.com (216.58.196.238) 56(84) bytes of data.

    --- google.com ping statistics ---
    60 packets transmitted, 60 received, 0% packet loss, time 59153ms
    rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms

Output
^^^^^^

.. code:: console

    ./parse_sample.py -f ping.txt
    # properties ---
    packet_transmit: 60
    packet_receive: 60
    packet_loss: 0.0
    rtt_min: 61.425
    rtt_avg: 99.731
    rtt_max: 212.597
    rtt_mdev: 27.566

    # asdict ---
    {
        "rtt_avg": 99.731,
        "packet_transmit": 60,
        "rtt_max": 212.597,
        "packet_loss": 0.0,
        "rtt_min": 61.425,
        "rtt_mdev": 27.566,
        "packet_receive": 60
    }

Example: Windows 10
~~~~~~~~~~~~~~~~~~~
Input
^^^^^

.. code:: console

    >ping google.com -n 10 > ping_win.txt

    >type ping_win.txt

    Pinging google.com [216.58.196.238] with 32 bytes of data:
    Reply from 216.58.196.238: bytes=32 time=87ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=97ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=56ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=95ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=194ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=98ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=93ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=96ms TTL=51
    Reply from 216.58.196.238: bytes=32 time=165ms TTL=51

    Ping statistics for 216.58.196.238:
        Packets: Sent = 10, Received = 10, Lost = 0 (0% loss),
    Approximate round trip times in milli-seconds:
        Minimum = 56ms, Maximum = 194ms, Average = 107ms

Output
^^^^^^

.. code:: console

    parse_sample.py -f ping_win.txt
    # properties ---
    packet_transmit: 10
    packet_receive: 10
    packet_loss: 0.0
    rtt_min: 56.0
    rtt_avg: 107.0
    rtt_max: 194.0
    rtt_mdev: None

    # asdict ---
    {
        "packet_loss": 0.0,
        "packet_transmit": 10,
        "rtt_min": 56.0,
        "rtt_avg": 107.0,
        "packet_receive": 10,
        "rtt_max": 194.0,
        "rtt_mdev": null
    }

Recommended ping command execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following methods are recommended to execute ``ping`` command for
parsing. These will change the locale setting to English temporarily.

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

   -  https://technet.microsoft.com/en-us/library/cc733037


Installation
============

::

    pip install pingparsing


Dependencies
============

Python 2.7+ or 3.3+

- `pyparsing <https://pyparsing.wikispaces.com/>`__
- `six <https://pypi.python.org/pypi/six/>`__
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
| Debian 8.6   | iputils-ping 20121221-5+b2        |
+--------------+-----------------------------------+
| Fedora 24    | iputils-20160308-3.fc24.x86\_64   |
+--------------+-----------------------------------+
| Windows 10   | ``-``                             |
+--------------+-----------------------------------+

Premise
=======

This library expects locale setup to English. Parsing the ``ping``
command output with any other locale may fail. This is because the
output of the ``ping`` command is changed depending on the locale
setting.

Documentation
=============

http://pingparsing.rtfd.io/

