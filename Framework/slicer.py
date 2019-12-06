
from abc import ABC, abstractmethod


class Slicer(ABC):

    def slice_line(self, revision_number: int, line_number: int):
        pass

    def handle_predecessors(self):
        pass

    def handle_success(self):
        pass

    def create_slice_subgraph(self, slicing_dict_nodes: dict):
        pass
