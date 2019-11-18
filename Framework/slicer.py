
from abc import ABC, abstractmethod

from Framework.node import Node


class Slicer(ABC):

    def slice(self, revision_number: int, line_number: int):
        pass
