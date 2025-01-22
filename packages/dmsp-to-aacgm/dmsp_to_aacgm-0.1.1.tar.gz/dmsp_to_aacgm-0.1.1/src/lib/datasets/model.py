from abc import ABC, abstractmethod
from typing import Any



class DataSet(ABC):

    @abstractmethod
    def match(data: Any) -> bool: ...

    @abstractmethod
    def convert(self): ...

    @abstractmethod
    def save(self, output_path: str): ...