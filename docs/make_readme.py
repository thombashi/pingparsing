#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import sys

import readmemaker


PROJECT_NAME = "pingparsing"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)

    maker.write_example_file("index.rst")


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR)
    maker.examples_dir_name = "usage"

    maker.write_introduction_file("badges.txt")

    maker.inc_indent_level()
    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")

    write_examples(maker)

    maker.write_file(
        maker.doc_page_root_dir_path.joinpath("installation.rst"))
    maker.write_file(
        maker.doc_page_root_dir_path.joinpath("introduction/premise.txt"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_line_list([
        "http://{:s}.readthedocs.org/en/latest/".format(PROJECT_NAME),
    ])

    return 0


if __name__ == '__main__':
    sys.exit(main())
