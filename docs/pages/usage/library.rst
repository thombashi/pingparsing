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
