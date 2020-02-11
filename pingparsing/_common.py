"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from typing import Union, cast


def _to_unicode(text: Union[str, bytes]) -> str:
    try:
        return text.decode("ascii")  # type: ignore
    except AttributeError:
        return cast(str, text)
