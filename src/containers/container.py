from typing import List
from abc import abstractmethod


class Container:
    """
    Represent an asset container.
    """

    @abstractmethod
    def add(self, items: List[str]):
        """
        Add assets.
        """

    @abstractmethod
    def process(self):
        """
        Process assets.
        """

    @abstractmethod
    def copy(self, to_path: str):
        """
        Copy assets.
        """
