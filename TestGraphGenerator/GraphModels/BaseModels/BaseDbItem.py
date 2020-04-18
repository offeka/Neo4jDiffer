from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import AnyStr


@dataclass
class BaseDbItem(metaclass=ABCMeta):
    @abstractmethod
    def generate_query_str(self) -> AnyStr:
        pass
