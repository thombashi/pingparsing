import abc
from typing import List

from ._stats import PingStats


class PingParserInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, ping_message: List[str]) -> PingStats:  # pragma: no cover
        pass
