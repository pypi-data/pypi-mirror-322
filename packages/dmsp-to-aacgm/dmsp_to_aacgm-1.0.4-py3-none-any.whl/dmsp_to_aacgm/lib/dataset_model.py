from abc import ABC, abstractmethod
from typing import Any, Optional



class DataSet(ABC):

    @abstractmethod
    def match(data: Any) -> bool: ...

    @abstractmethod
    def convert(self): ...

    @abstractmethod
    def close(self): ...