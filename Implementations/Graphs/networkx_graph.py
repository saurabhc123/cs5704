import networkx as nx

from Framework.graph import Graph
from Framework.node import Node
from Framework.serializer import Serializer


class NetworkxGraph(Graph):

    def __init__(self, serializer: Serializer = None):
        self.G = nx.MultiDiGraph()
        self.serializer = serializer

    def add_node(self, node: Node, node_id: str):
        self.G.add_node(node, id=node_id)

    def add_edge(self, left_node: Node, new_right_node: Node):
        self.G.add_edge(left_node, new_right_node)

    def out_degree(self, left_node: Node):
        return self.G.out_degree(left_node)

    def find_node_in_graph(self, node_id):
        for (key, value) in self.G.nodes(data=True):
            if value['id'] == node_id:
                return key
        return None

    def serialize_graph(self):
        graph_edges = list(self.G.edges)
        edge_tuples = []
        for edge in graph_edges:
            left_node = edge[0]
            right_node = edge[1]
            label = right_node.label
            edge_tuples.append((left_node, right_node, label))

        self.serializer.serialize(edge_tuples)
