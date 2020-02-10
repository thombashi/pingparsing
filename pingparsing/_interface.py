import abc


class PingParserInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, ping_message):  # pragma: no cover
        pass
