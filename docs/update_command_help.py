#!/usr/bin/env python3

import os
import sys
from textwrap import indent

from subprocrunner import CalledProcessError, SubprocessRunner


def main():
    proc = SubprocessRunner(["pingparsing", "-h"])
    try:
        proc.run(env=dict(os.environ, LC_ALL="C.UTF-8"), check=True)
    except CalledProcessError as e:
        print(f"[ERROR] {e}\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

    help_file_path = "pages/usage/cli_help.txt"

    print(help_file_path)

    with open(help_file_path, "w") as f:
        f.write("CLI help\n")
        f.write("--------------------------------------------\n")
        f.write("::\n\n")
        f.write(indent(proc.stdout, "    "))


if __name__ == "__main__":
    main()
