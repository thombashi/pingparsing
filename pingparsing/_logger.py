"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import subprocrunner


MODULE_NAME = "pingparsing"


class NullLogger(object):
    level_name = None

    def critical(self, *args, **kwargs):  # pragma: no cover
        pass

    def debug(self, *args, **kwargs):  # pragma: no cover
        pass

    def disable(self, name):  # pragma: no cover
        pass

    def enable(self, name):  # pragma: no cover
        pass

    def error(self, *args, **kwargs):  # pragma: no cover
        pass

    def exception(self, *args, **kwargs):  # pragma: no cover
        pass

    def info(self, *args, **kwargs):  # pragma: no cover
        pass

    def log(self, level, *args, **kwargs):  # pragma: no cover
        pass

    def notice(self, *args, **kwargs):  # pragma: no cover
        pass

    def success(self, *args, **kwargs):  # pragma: no cover
        pass

    def trace(self, *args, **kwargs):  # pragma: no cover
        pass

    def warning(self, *args, **kwargs):  # pragma: no cover
        pass


try:
    from loguru import logger

    logger.disable(MODULE_NAME)
except ImportError:
    logger = NullLogger()  # type: ignore


def set_logger(is_enable, propagation_depth=1):
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)

    if propagation_depth <= 0:
        return

    subprocrunner.set_logger(is_enable, propagation_depth - 1)


def set_log_level(log_level):
    # deprecated
    return
