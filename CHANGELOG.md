<a name="v1.4.1"></a>
# [v1.4.1](https://github.com/thombashi/pingparsing/releases/tag/v1.4.1) - 18 Feb 2023

## What's Changed
- Fix Pygemnts requirement in setup.py by [@s-t-e-v-e-n-k](https://github.com/s-t-e-v-e-n-k) in https://github.com/thombashi/pingparsing/pull/47
- Change the output of the CLI logger to stderr
- Add support for Python 3.11
- Update help messages
- Update requirements

## New Contributors
* [@s-t-e-v-e-n-k](https://github.com/s-t-e-v-e-n-k) made their first contribution in https://github.com/thombashi/pingparsing/pull/47

**Full Changelog**: https://github.com/thombashi/pingparsing/compare/v1.4.0...v1.4.1

[Changes][v1.4.1]


<a name="v1.4.0"></a>
# [v1.4.0](https://github.com/thombashi/pingparsing/releases/tag/v1.4.0) - 24 Oct 2021

- Drop support for Python 3.5
- Add support for `pyparsing` v3


[Changes][v1.4.0]


<a name="v1.3.2"></a>
# [v1.3.2](https://github.com/thombashi/pingparsing/releases/tag/v1.3.2) - 02 Jun 2021

- Fix parsing when ping results with `pipe` field: [#45](https://github.com/thombashi/pingparsing/issues/45) (Thanks to [@docweirdo](https://github.com/docweirdo))


[Changes][v1.3.2]


<a name="v1.3.1"></a>
# [v1.3.1](https://github.com/thombashi/pingparsing/releases/tag/v1.3.1) - 05 May 2021

- Change `PingTransmitter.ping_option` accepts `Sequence`
- Fix a problem that `--interface` option value is not properly applied to ping commands


[Changes][v1.3.1]


<a name="v1.3.0"></a>
# [v1.3.0](https://github.com/thombashi/pingparsing/releases/tag/v1.3.0) - 27 Mar 2021

- Add packet size in `icmp_replies`: [#35](https://github.com/thombashi/pingparsing/issues/35) (Thanks to [@cloudprodz](https://github.com/cloudprodz))
- Add received addresses in `icmp_replies`: [#38](https://github.com/thombashi/pingparsing/issues/38) (Thanks to [@vi](https://github.com/vi))
- Fix incorrect parsing of destination domain with `'.net'` suffix: [#40](https://github.com/thombashi/pingparsing/issues/40) (Thanks to [@xNathan](https://github.com/xNathan))
- Fix parsing of Windows ping replies
- Modify a type annotation of `PingParserInterface.parse` method
- Improve parsing precision of times

[Changes][v1.3.0]


<a name="v1.2.0"></a>
# [v1.2.0](https://github.com/thombashi/pingparsing/releases/tag/v1.2.0) - 31 Jan 2021

- Add support for Python 3.10
- Add `--timezone` option to the CLI
- Add time zone support for parser classes


[Changes][v1.2.0]


<a name="v1.1.0"></a>
# [v1.1.0](https://github.com/thombashi/pingparsing/releases/tag/v1.1.0) - 09 Aug 2020

- Make it possible to parse ping timeouts includes timestamps: [#37](https://github.com/thombashi/pingparsing/issues/37) (Thanks to [@banananananananana](https://github.com/banananananananana))
- Add `--addopts` option to the CLI
- Add `-O` option to ping execution when `--timestamp` option is specified on Linux
- Set default serializer for timestamps of ICMP replies


[Changes][v1.1.0]


<a name="v1.0.3"></a>
# [v1.0.3](https://github.com/thombashi/pingparsing/releases/tag/v1.0.3) - 26 Apr 2020

- Fix type annotations
- Update requirements

[Changes][v1.0.3]


<a name="v1.0.2"></a>
# [v1.0.2](https://github.com/thombashi/pingparsing/releases/tag/v1.0.2) - 04 Apr 2020

- Make it possible to execute the CLI with `python -m pingparsing`
- Update requirements


[Changes][v1.0.2]


<a name="v1.0.0"></a>
# [v1.0.0](https://github.com/thombashi/pingparsing/releases/tag/v1.0.0) - 23 Feb 2020

- Drop Python 2 support
- Add packet size option to `PingTransmitter` and CLI: [#34](https://github.com/thombashi/pingparsing/issues/34) (Thanks to [@salehdeh76](https://github.com/salehdeh76))
- Add `ttl` option to `PingTransmitter` and CLI: [#34](https://github.com/thombashi/pingparsing/issues/34) (Thanks to [@salehdeh76](https://github.com/salehdeh76))
- Add `include_icmp_replies` flag to `PingStats.as_dict` method
- Add `--no-color` option to the CLI tool
- Add type annotations and `py.typed` to the package
- Add `[cli]` extras_require
- Update dependencies
- Remove deprecated methods
- Reduce a package dependency
- Replace the logging library
- Fix timestamp parsing when transmitting ping by CLI
- Minor bug fixes

[Changes][v1.0.0]


<a name="v0.18.2"></a>
# [v0.18.2](https://github.com/thombashi/pingparsing/releases/tag/v0.18.2) - 04 Jan 2020

- Fix parsing failed when ping transmit failure: [#33](https://github.com/thombashi/pingparsing/issues/33) (Thanks to [@psmorris](https://github.com/psmorris))
- Integrate `build`/`release`/`docs` extras to `dev` extras
- Add `.asc` files of packages to PyPI
- Update requirements


[Changes][v0.18.2]


<a name="v0.18.0"></a>
# [v0.18.0](https://github.com/thombashi/pingparsing/releases/tag/v0.18.0) - 11 May 2019

- Add `timestamp` attribute to `PingTransmitter` class
- Add `--timestamp` option to the CLI
- Add support for Python 3.8
- Support timestamp sub-second precision: [#29](https://github.com/thombashi/pingparsing/issues/29) (Thanks to [@marty90](https://github.com/marty90))


[Changes][v0.18.0]


<a name="v0.16.0"></a>
# [v0.16.0](https://github.com/thombashi/pingparsing/releases/tag/v0.16.0) - 17 Mar 2019

- Enhancements:
    - accept human-readable values for timeout/deadline
    - use colorized logging
    - improve logging


[Changes][v0.16.0]


<a name="v0.15.0"></a>
# [v0.15.0](https://github.com/thombashi/pingparsing/releases/tag/v0.15.0) - 17 Feb 2019

- Rename from `icmp_reply` to `icmp_relies`
- Fix parsing from stdin
- Fix parsing for each reply failed when source includes other than IP address


[Changes][v0.15.0]


<a name="v0.14.0"></a>
# [v0.14.0](https://github.com/thombashi/pingparsing/releases/tag/v0.14.0) - 12 Feb 2019

- Add support for `timeout`: [#31](https://github.com/thombashi/pingparsing/issues/31) (Thanks to [@ChristofKaufmann](https://github.com/ChristofKaufmann))

[Changes][v0.14.0]


<a name="v0.13.0"></a>
# [v0.13.0](https://github.com/thombashi/pingparsing/releases/tag/v0.13.0) - 29 Apr 2018

- Add support for parsing ICMP replies (Thanks to [@geokal](https://github.com/geokal))
- Bug fixes

[Changes][v0.13.0]


<a name="v0.12.1"></a>
# [v0.12.1](https://github.com/thombashi/pingparsing/releases/tag/v0.12.1) - 07 Apr 2018

- Fix the case that duplicate packet statistics not properly parsed
- Fix the deadline option not properly worked at macOS


[Changes][v0.12.1]


<a name="v0.12.0"></a>
# [v0.12.0](https://github.com/thombashi/pingparsing/releases/tag/v0.12.0) - 05 Nov 2017

- Add `pingparsing` CLI
- Add `as_tuple` method to `PingParsing` class
- Change `PingParsing.parse` method to return the parsed result as `namedtuple`
- Improve log messages
- Drop support for Python 3.3


[Changes][v0.12.0]


<a name="v0.11.0"></a>
# [v0.11.0](https://github.com/thombashi/pingparsing/releases/tag/v0.11.0) - 21 Oct 2017

- Add ping `destination` as a parsing target
- Take into effect `interface` attribute for `PingTransmitter` class
- Add OS X support for ping transmitter: [#28](https://github.com/thombashi/pingparsing/issues/28) (Thanks to [@mozillazg](https://github.com/mozillazg))
- Modify Alpine Linux parser to properly parse packet duplicates
- Bug fixes

[Changes][v0.11.0]


<a name="v0.10.0"></a>
# [v0.10.0](https://github.com/thombashi/pingparsing/releases/tag/v0.10.0) - 13 Sep 2017

- Add a ping parser for Alpine Linux: [#27](https://github.com/thombashi/pingparsing/issues/27) ([@maikotz](https://github.com/maikotz))


[Changes][v0.10.0]


<a name="v0.9.0"></a>
# [v0.9.0](https://github.com/thombashi/pingparsing/releases/tag/v0.9.0) - 02 Aug 2017

- Add a ping parser for OSX: [#26](https://github.com/thombashi/pingparsing/issues/26) (Thanks to [@marchon](https://github.com/marchon))
- Bug fixes


[Changes][v0.9.0]


<a name="v0.8.2"></a>
# [v0.8.2](https://github.com/thombashi/pingparsing/releases/tag/v0.8.2) - 11 Jun 2017

- Change to `PingParsing.parse` method accept `PingResult` instance as an input: [#25](https://github.com/thombashi/pingparsing/issues/25) (Thanks to [@L1ghtn1ng](https://github.com/L1ghtn1ng) )



[Changes][v0.8.2]


<a name="v0.8.0"></a>
# [v0.8.0](https://github.com/thombashi/pingparsing/releases/tag/v0.8.0) - 04 Jun 2017

- Add duplicate_rate attribute
- Add packet_loss_count attribute
- Improve packet loss rate precision
- Add log messages


[Changes][v0.8.0]


<a name="v0.6.0"></a>
# [v0.6.0](https://github.com/thombashi/pingparsing/releases/tag/v0.6.0) - 28 Mar 2017

- Add `duplicates` property to PingParsing class to get number of duplicated packets (Thanks to Mengying Xiong)

[Changes][v0.6.0]


<a name="v0.5.0"></a>
# [v0.5.0](https://github.com/thombashi/pingparsing/releases/tag/v0.5.0) - 22 Mar 2017

- Add IPv6 support 
- [#24](https://github.com/thombashi/pingparsing/issues/24): Fix ``count`` attribute not properly applied (Thanks to [@bladernr](https://github.com/bladernr))


[Changes][v0.5.0]


<a name="v0.4.0"></a>
# [v0.4.0](https://github.com/thombashi/pingparsing/releases/tag/v0.4.0) - 11 Dec 2016

- Change behaviour of waittime: [#21](https://github.com/thombashi/pingparsing/issues/21) Thanks to [@toddjames](https://github.com/toddjames) 
- Add count property to PingTransmitter class: [#22](https://github.com/thombashi/pingparsing/issues/22) Thanks to [@toddjames](https://github.com/toddjames) 
- Bug fixes


[Changes][v0.4.0]


<a name="v0.3.0"></a>
# [v0.3.0](https://github.com/thombashi/pingparsing/releases/tag/v0.3.0) - 15 Oct 2016

- Fix parse failure when ping statistics is empty
- Fix PingTransmitter to continue processing when ping failed
- Bug fixes
- Add examples


[Changes][v0.3.0]


<a name="v0.2.9"></a>
# [v0.2.9](https://github.com/thombashi/pingparsing/releases/tag/v0.2.9) - 12 Aug 2016

- Fix for the case that occurs packet loss


[Changes][v0.2.9]


<a name="v0.2.8"></a>
# [v0.2.8](https://github.com/thombashi/pingparsing/releases/tag/v0.2.8) - 26 Jul 2016

- Drop support for Python 2.6


[Changes][v0.2.8]


<a name="v0.2.7"></a>
# [v0.2.7](https://github.com/thombashi/pingparsing/releases/tag/v0.2.7) - 19 Jun 2016

- Make pytest-runner a conditional requirement
- Drop support for Python 2.5


[Changes][v0.2.7]


<a name="v0.2.6"></a>
# [v0.2.6](https://github.com/thombashi/pingparsing/releases/tag/v0.2.6) - 19 Mar 2016



[Changes][v0.2.6]


<a name="v0.2.5"></a>
# [v0.2.5](https://github.com/thombashi/pingparsing/releases/tag/v0.2.5) - 12 Mar 2016



[Changes][v0.2.5]


[v1.4.1]: https://github.com/thombashi/pingparsing/compare/v1.4.0...v1.4.1
[v1.4.0]: https://github.com/thombashi/pingparsing/compare/v1.3.2...v1.4.0
[v1.3.2]: https://github.com/thombashi/pingparsing/compare/v1.3.1...v1.3.2
[v1.3.1]: https://github.com/thombashi/pingparsing/compare/v1.3.0...v1.3.1
[v1.3.0]: https://github.com/thombashi/pingparsing/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/thombashi/pingparsing/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/thombashi/pingparsing/compare/v1.0.3...v1.1.0
[v1.0.3]: https://github.com/thombashi/pingparsing/compare/v1.0.2...v1.0.3
[v1.0.2]: https://github.com/thombashi/pingparsing/compare/v1.0.0...v1.0.2
[v1.0.0]: https://github.com/thombashi/pingparsing/compare/v0.18.2...v1.0.0
[v0.18.2]: https://github.com/thombashi/pingparsing/compare/v0.18.0...v0.18.2
[v0.18.0]: https://github.com/thombashi/pingparsing/compare/v0.16.0...v0.18.0
[v0.16.0]: https://github.com/thombashi/pingparsing/compare/v0.15.0...v0.16.0
[v0.15.0]: https://github.com/thombashi/pingparsing/compare/v0.14.0...v0.15.0
[v0.14.0]: https://github.com/thombashi/pingparsing/compare/v0.13.0...v0.14.0
[v0.13.0]: https://github.com/thombashi/pingparsing/compare/v0.12.1...v0.13.0
[v0.12.1]: https://github.com/thombashi/pingparsing/compare/v0.12.0...v0.12.1
[v0.12.0]: https://github.com/thombashi/pingparsing/compare/v0.11.0...v0.12.0
[v0.11.0]: https://github.com/thombashi/pingparsing/compare/v0.10.0...v0.11.0
[v0.10.0]: https://github.com/thombashi/pingparsing/compare/v0.9.0...v0.10.0
[v0.9.0]: https://github.com/thombashi/pingparsing/compare/v0.8.2...v0.9.0
[v0.8.2]: https://github.com/thombashi/pingparsing/compare/v0.8.0...v0.8.2
[v0.8.0]: https://github.com/thombashi/pingparsing/compare/v0.6.0...v0.8.0
[v0.6.0]: https://github.com/thombashi/pingparsing/compare/v0.5.0...v0.6.0
[v0.5.0]: https://github.com/thombashi/pingparsing/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/thombashi/pingparsing/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/thombashi/pingparsing/compare/v0.2.9...v0.3.0
[v0.2.9]: https://github.com/thombashi/pingparsing/compare/v0.2.8...v0.2.9
[v0.2.8]: https://github.com/thombashi/pingparsing/compare/v0.2.7...v0.2.8
[v0.2.7]: https://github.com/thombashi/pingparsing/compare/v0.2.6...v0.2.7
[v0.2.6]: https://github.com/thombashi/pingparsing/compare/v0.2.5...v0.2.6
[v0.2.5]: https://github.com/thombashi/pingparsing/tree/v0.2.5

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.7.2 -->
