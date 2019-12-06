from abc import ABC, abstractmethod
from Framework.node import Node


class GraphBuilder(ABC):

    def build_graph(self, revisions):
        pass

    def slice(self, revision_number, line_number):
        nodes, content_id = self.slicer.slice_line(revision_number, line_number)

        self.visualize_subgraph(nodes)

        return nodes, content_id

    def visualize_subgraph(self, nodes_dict:dict):
        for i in sorted(nodes_dict.keys()):
            print(i.get_node_id())
        # keys_list = list(nodes_dict.keys())
        #
        # revision_number, line_number =

