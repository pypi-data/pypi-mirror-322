from abc import ABC, abstractmethod
from typing import Any, Optional



class DataSet(ABC):

    @abstractmethod
    def match(data: Any) -> bool: ...

    @abstractmethod
    def convert(self, output_path: Optional[str] = None): ...

    @abstractmethod
    def close(self): ...