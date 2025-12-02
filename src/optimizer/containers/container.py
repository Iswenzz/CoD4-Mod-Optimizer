from typing import List
from abc import abstractmethod


class Container:

    @abstractmethod
    def add(self, items: List[str]): ...

    @abstractmethod
    def process(self): ...

    @abstractmethod
    def copy(self, to_path: str): ...
