from abc import ABC, abstractmethod

from Framework.input_source import InputSource
from Framework.node import Node


class Mapper(ABC):

    def initialize_mappings(self, revisions):
        pass

    def get_mapping(self, left_line_number: int, right_line_number: int, left_revision_number):
        pass