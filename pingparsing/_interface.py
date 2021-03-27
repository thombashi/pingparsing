import abc
from typing import Sequence

from ._stats import PingStats


class PingParserInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, ping_message: Sequence[str]) -> PingStats:  # pragma: no cover
        pass
