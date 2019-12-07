
from Framework.slicer import Slicer
from Framework.graph import Graph
from Framework.node import Node


class LineSlicer(Slicer):

    def __init__(self, graph: Graph):
        self.G = graph


    # criterion should be starting_line, ending_line, staring_rev, ending_rev
    def slice_line(self, revision_number: int, line_number: int):
        starting_node_id = str(revision_number) + "." + str(line_number)
        starting_node = self.G.find_node_in_graph(starting_node_id)

        slicing_dict_nodes = dict()
        slicing_dict_content_by_id = dict()

        starting_node_index = starting_node.get_node_id() + "***" + starting_node.content
        slicing_dict_content_by_id[starting_node_index] = []
        slicing_dict_nodes[starting_node] = []

        for p in self.G.predecessors(starting_node):
            slicing_dict_nodes[p] = []
            slicing_dict_nodes[p].append(starting_node)
            p_index = p.get_node_id() + "***" + p.content
            slicing_dict_content_by_id[p_index] = []
            slicing_dict_content_by_id[p_index].append(starting_node_index)
            self.handle_predecessors(p, slicing_dict_nodes, slicing_dict_content_by_id)

        for s in self.G.successors(starting_node):
            slicing_dict_nodes[starting_node].append(s)
            slicing_dict_nodes[s] = []
            s_index = s.get_node_id() + "***" + s.content
            slicing_dict_content_by_id[starting_node_index].append(s_index)
            slicing_dict_content_by_id[s_index] = []
            self.handle_successors(s, slicing_dict_nodes, slicing_dict_content_by_id)

        self.create_slice_subgraph(slicing_dict_nodes)

        return slicing_dict_nodes, slicing_dict_content_by_id

    def handle_successors(self, succ_node: Node, nodes_dict: dict, content_dict: dict):
        for s in self.G.successors(succ_node):
            nodes_dict[succ_node].append(s)
            nodes_dict[s] = []
            s_index = s.get_node_id() + "***" + s.content
            content_dict[s_index] = []
            content_dict[succ_node.get_node_id() + "***" + succ_node.content].append(s_index)
            self.handle_successors(s, nodes_dict, content_dict)

    def handle_predecessors(self, pred_node: Node, nodes_dict: dict, content_dict: dict):
        for p in self.G.predecessors(pred_node):
            nodes_dict[p] = []
            nodes_dict[p].append(pred_node)
            p_index = p.get_node_id() + "***" + p.content
            content_dict[p_index] = []
            content_dict[p_index].append(pred_node.get_node_id() + "***" + pred_node.content)
            self.handle_predecessors(p, nodes_dict, content_dict)

    def create_slice_subgraph(self, slicing_dict_nodes: dict):
        self.sub_graph: Graph = self.G
        self.sub_graph.clear()

        nodes = list(slicing_dict_nodes.keys())

        for n in nodes:
            self.sub_graph.add_node(n, node_id=n.get_node_id())

        for n in nodes:
            nodes_succs = slicing_dict_nodes[n]
            curr_node = self.sub_graph.find_node_in_graph(n.get_node_id())

            for s in nodes_succs:
                succ_node = self.sub_graph.find_node_in_graph(s.get_node_id())
                self.sub_graph.add_edge(curr_node, succ_node)

    def slice(self, revision_number, line_number):
        nodes, content_id = self.slice_line(revision_number, line_number)

        self.visualize_subgraph(nodes)

        return nodes, content_id

    def visualize_subgraph(self, nodes_dict:dict):
        for i in sorted(nodes_dict.keys()):
            print(i.get_node_id())
        # keys_list = list(nodes_dict.keys())
        #
        # revision_number, line_number =


