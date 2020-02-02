"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


def _to_unicode(text):
    try:
        return text.decode("ascii")
    except AttributeError:
        return text
