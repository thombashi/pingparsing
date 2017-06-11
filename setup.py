# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import io
import os.path
import sys

import setuptools


REQUIREMENT_DIR = "requirements"

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []


with io.open("README.rst", encoding="utf8") as fp:
    long_description = fp.read()

with io.open(os.path.join(
        "docs", "pages", "introduction", "summary.txt"), encoding="utf8") as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    install_requires.append("ipaddress")

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_require = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="pingparsing",
    version="0.8.2",
    author="Tsuyoshi Hombashi",
    author_email="gogogo.vm@gmail.com",
    url="https://github.com/thombashi/pingparsing",
    keywords=["ping", "parser", "transmitter"],
    license="MIT License",
    description=summary,
    long_description=long_description,
    include_package_data=True,
    install_requires=install_requires,
    packages=setuptools.find_packages(exclude=["test*"]),
    setup_requires=pytest_runner,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)
