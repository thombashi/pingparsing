**pingparsing**

.. image:: https://travis-ci.org/thombashi/pingparsing.svg?branch=master
    :target: https://travis-ci.org/thombashi/pingparsing

.. contents:: Table of contents
   :backlinks: top
   :local:

Summary
=======
pingparsing is a python library of parsing ping command output.

Installation
============

::

    pip install pingparsing

Premise
=======

Output language of the ping command is in english.

Usage
=====

Parsing ping output
-------------------

Example: parse ping output of debian 8.2 w/ iputils-ping 20121221-5+b2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``parse_sample.py``

.. code:: python

    import pingparsing
    ping_parser = pingparsing.PingParsing()

    # parse out put of `ping google.com -q -c 60`
    ping_parser.parse("""
    PING google.com (216.58.196.238) 56(84) bytes of data.

    --- google.com ping statistics ---
    60 packets transmitted, 60 received, 0% packet loss, time 59153ms
    rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
    """)

    print "packet_transmit:", ping_parser.packet_transmit
    print "packet_receive:", ping_parser.packet_receive
    print "packet_loss:", ping_parser.packet_loss
    print "rtt_min:", ping_parser.rtt_min
    print "rtt_avg:", ping_parser.rtt_avg
    print "rtt_max:", ping_parser.rtt_max
    print "rtt_mdev:", ping_parser.rtt_mdev
    print ping_parser.as_dict()

.. code:: console

    ./parse_sample.py
    packet_transmit: 60
    packet_receive: 60
    packet_loss: 0.0
    rtt_min: 61.425
    rtt_avg: 99.731
    rtt_max: 212.597
    rtt_mdev: 27.566
    {'packet_loss': 0.0, 'packet_receive': 60, 'packet_transmit': 60, 'rtt_min': 61.425, 'rtt_max': 212.597, 'rtt_mdev': 27.566, 'rtt_avg': 99.731}

Example: parse ping output of Windows 7 SP1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``parse_sample.py``

.. code:: python

    #!/usr/bin/env python
    import pingparsing
    ping_parser = pingparsing.PingParsing()

    # parse out put of `ping google.com -n 10`
    ping_parser.parse("""
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
    """)

    print ping_parser.as_dict()

.. code:: console

    ./parse_sample.py
    {'packet_loss': 0.0, 'packet_receive': 10, 'packet_transmit': 10, 'rtt_min': 56.0, 'rtt_max': 194.0, 'rtt_mdev': None, 'rtt_avg': 107.0}

Execute ping and parse
----------------------

Example code
~~~~~~~~~~~~

``ping_sample.py``

.. code:: python

    import pingparsing
    ping_parser = pingparsing.PingParsing()
    ping_parser.destination_host = "192.168.0.1"
    ping_parser.waittime = 60
    result = ping_parser.ping()
    ping_parser.parse(result)

    print ping_parser.as_dict()

Example execution result: Debian 8.2 w/ iputils-ping 20121221-5+b2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    # python ping_sample.py
    {'packet_loss': 0.0, 'packet_receive': 60, 'packet_transmit': 60, 'rtt_min': 0.814, 'rtt_max': 27.958, 'rtt_mdev': 3.574, 'rtt_avg': 2.004}

Example execution result: Windows 7 SP1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    >python ping_sample.py
    Minimum = 0ms, Maximum = 56ms, Average = 2ms
    {'packet_loss': 0.0, 'packet_receive': 60, 'packet_transmit': 60, 'rtt_min': 0.0
    , 'rtt_max': 56.0, 'rtt_mdev': None, 'rtt_avg': 2.0}

Dependencies
============

Python 2.5+ or 3.3+

-  `DataPropery <https://github.com/thombashi/DataProperty>`__
-  `pyparsing <https://pyparsing.wikispaces.com/>`__

Test dependencies
-----------------

-  `pytest <https://pypi.python.org/pypi/pytest>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://pypi.python.org/pypi/tox>`__

Tested Environment
==================

+-----------------+----------------------------------+
| OS              | ping version                     |
+=================+==================================+
| Debian 8.2      | iputils-ping 20121221-5+b2       |
+-----------------+----------------------------------+
| Debian 5.0.10   | iputils-ping 20071127-1+lenny1   |
+-----------------+----------------------------------+
| Windows 7 SP1   | ``-``                            |
+-----------------+----------------------------------+
| Windows 8.1     | ``-``                            |
+-----------------+----------------------------------+
