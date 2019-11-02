import networkx as nx

from Framework.graph import Graph
from Framework.node import Node


class NetworkxGraph(Graph):

    def __init__(self):
        self.G = nx.MultiDiGraph()
        #NetworkxGraph.G = self.G

    def add_node(self, node: Node, node_id: str):
        #print(node_id)
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