#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, unicode_literals

import os
from textwrap import indent

from subprocrunner import SubprocessRunner


proc = SubprocessRunner(["pingparsing", "-h"])
proc.run(env=dict(os.environ, LC_ALL="C.UTF-8"))
help_file_path = "pages/usage/cli_help.txt"

print(help_file_path)

with open(help_file_path, "w") as f:
    f.write("CLI help\n")
    f.write("--------------------------------------------\n")
    f.write("::\n\n")
    f.write(indent(proc.stdout, "    "))
