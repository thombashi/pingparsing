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
        ping_parser.parse(result)
        print(json.dumps(ping_parser.as_dict(), indent=4))

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
        import pingparsing

        parser = pingparsing.PingParsing()
        parser.parse("""PING google.com (216.58.196.238) 56(84) bytes of data.

        --- google.com ping statistics ---
        60 packets transmitted, 60 received, 0% packet loss, time 59153ms
        rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
        """)
        print(json.dumps(parser.as_dict(), indent=4))

:Output:
    .. code-block:: json

        {
            "destination": "google.com",
            "packet_transmit": 60,
            "packet_receive": 60,
            "packet_loss_rate": 0.0,
            "packet_loss_count": 0,
            "rtt_min": 61.425,
            "rtt_avg": 99.731,
            "rtt_max": 212.597,
            "rtt_mdev": 27.566,
            "packet_duplicate_rate": 0.0,
            "packet_duplicate_count": 0
        }

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
