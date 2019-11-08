from abc import ABC, abstractmethod

from Framework.node import Node


class Graph(ABC):

    def add_node(self, node: Node, node_id: str):
        pass

    def add_edge(self, left_node: Node, new_right_node: Node):
        pass

    def out_degree(self, left_node: Node):
        pass

    def find_node_in_graph(self, node_id):
        pass

    def serialize_graph(self):
        pass
