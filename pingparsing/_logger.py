"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import subprocrunner


MODULE_NAME = "pingparsing"


class NullLogger:
    level_name = None

    def remove(self, handler_id=None):  # pragma: no cover
        pass

    def add(self, sink, **kwargs):  # pragma: no cover
        pass

    def disable(self, name):  # pragma: no cover
        pass

    def enable(self, name):  # pragma: no cover
        pass

    def critical(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def debug(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def error(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def exception(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def info(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def log(self, __level, __message, *args, **kwargs):  # pragma: no cover
        pass

    def success(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def trace(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def warning(self, __message, *args, **kwargs):  # pragma: no cover
        pass


try:
    from loguru import logger

    logger.disable(MODULE_NAME)
except ImportError:
    logger = NullLogger()  # type: ignore


def set_logger(is_enable: bool, propagation_depth: int = 1) -> None:
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)

    if propagation_depth <= 0:
        return

    subprocrunner.set_logger(is_enable, propagation_depth - 1)


def set_log_level(log_level):
    # deprecated
    logger.disable(MODULE_NAME)
