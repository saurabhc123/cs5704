from Framework.graph import Graph
from Framework.node import Node
import networkx as nx
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz


class GraphBuilder():

    def __init__(self, matcher, graph: Graph):
        self.graph = graph
        self.matcher = matcher
        pass

    def build_graph(self, revisions):
        first_revision = revisions[0]
        starting_nodes = self.initialize_first_revision(first_revision)
        print(starting_nodes)
        history_graph = [starting_nodes]
        for revision_number in range(1, len(revisions)):
            starting_nodes = self.build_graph_from_subsequent_revisions(starting_nodes, revisions[revision_number],
                                                                        revision_number)
            history_graph.append(starting_nodes)
        return history_graph

    def build_graph_from_subsequent_revisions(self, left_nodes, right: [str], revision_number):
        ptr_left = 0
        ptr_right = 0
        right_nodes = []
        while True:
            # if no more to process on the right side and the left side
            if ptr_left >= len(left_nodes) and ptr_right >= len(right):
                break

            # if no more to process on the left side, but more on the right side
            # Iterate through the right nodes, and add all of them (added) as the right nodes array and the graph
            if ptr_left >= len(left_nodes) and ptr_right < len(right):
                for i in range(ptr_right, len(right)):
                    new_right_node = Node("a", ptr_right + 1, right[ptr_right], revision_number + 1)
                    self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
                    right_nodes.append(new_right_node)
                break

            # If more to process on the left side and no more to process on the right side,
            # Iterate through the left nodes, and mark all of them as (deleted) the left nodes array.
            # Find the left node on the graph. Change its label.
            if ptr_left < len(left_nodes) and ptr_right >= len(right):
                for i in range(ptr_left, len(left_nodes)):
                    if self.graph.out_degree(left_nodes[i]) > 0:
                        continue
                    graph_node = self.get_node_from_graph(left_nodes, ptr_left)
                    # graph_node = list(self.G.nodes)[int(self.G.nodes[left_nodes[i]]['id']) - 1]
                    graph_node.label = "d"
                break

            left_node = left_nodes[ptr_left]
            if self.matcher.evaluate_match(left_node.content, right[ptr_right]) == 'u':
                new_right_node = Node("u", ptr_right + 1, right[ptr_right], revision_number + 1)
                self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
                self.graph.add_edge(left_node, new_right_node)
                right_nodes.append(new_right_node)
                ptr_left = ptr_left + 1
                ptr_right = ptr_right + 1
                continue

            if self.matcher.evaluate_match(left_node.content, right[ptr_right]) == 'c':
                new_right_node = Node("c", ptr_right + 1, right[ptr_right], revision_number + 1)
                self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
                self.graph.add_edge(left_node, new_right_node)
                right_nodes.append(new_right_node)
                ptr_right = ptr_right + 1
                continue

                # Unmatched
            if self.graph.out_degree(left_node) > 0:
                ptr_left = ptr_left + 1
                continue

            ptr_left, ptr_right = self.handle_unmatched(ptr_left, ptr_right, left_nodes, right, right_nodes)

        return right_nodes

    def handle_unmatched(self, ptr_left: int, ptr_right: int, left_nodes: [Node], right, right_nodes: [Node]):
        left_revision_number = left_nodes[ptr_left].revision_number
        right_revision_number = left_revision_number + 1
        # Increment the left ptr
        ptr_left = ptr_left + 1
        # If left_ptr out of bounds
        if ptr_left >= len(left_nodes):
            ptr_left = ptr_left - 1
            # right is an "a" add to graph
            new_right_node = Node("a", ptr_right + 1, right[ptr_right], right_revision_number)
            self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
            right_nodes.append(new_right_node)
            # move right ptr by 1
            ptr_right = ptr_right + 1
            return ptr_left, ptr_right
        # Compare left_ptr and right
        left_node = left_nodes[ptr_left]
        match_status = self.matcher.evaluate_match(left_node.content, right[ptr_right])
        if "unmatched" in match_status:
            # Unmatched
            # Create right node as "a" and add to the graph
            # Add to the right_nodes list
            # left_node_to_be_changed = self.get_node_from_graph(left_nodes, ptr_left - 1)
            # left_node_to_be_changed.label = "d"
            new_right_node = Node("a", ptr_right + 1, right[ptr_right], right_revision_number)
            self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
            right_nodes.append(new_right_node)
            ptr_right = ptr_right + 1
            ptr_left = ptr_left - 1
            return ptr_left, ptr_right
        else:
            # Mark left_ptr - 1 as "d"
            left_node_to_be_changed = self.get_node_from_graph(left_nodes, ptr_left - 1)
            left_node_to_be_changed.label = "d"
            if "c" in match_status:
                # Create right node as "c" and add to the graph
                new_right_node = Node("c", ptr_right + 1, right[ptr_right], right_revision_number)
                self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
                # Add to the right_nodes list
                right_nodes.append(new_right_node)
                # Add an edge between left_ptr and right_ptr + 1
                self.graph.add_edge(left_node, new_right_node)
                # Increment right_ptr by 1
                ptr_right = ptr_right + 1
                return ptr_left, ptr_right
            else:
                # Create right node as "u" and add to the graph
                new_right_node = Node("u", ptr_right + 1, right[ptr_right], right_revision_number)
                self.graph.add_node(new_right_node, node_id=new_right_node.get_node_id())
                # Add to the right_nodes list
                right_nodes.append(new_right_node)
                # Add an edge between left_ptr and right_ptr + 1
                self.graph.add_edge(left_node, new_right_node)
                # Increment left_ptr and right_ptr by 1
                ptr_right = ptr_right + 1
                ptr_left = ptr_left + 1
                return ptr_left, ptr_right

    def get_node_from_graph(self, left_nodes, ptr_left):
        node_id_to_search = left_nodes[ptr_left].get_node_id()
        return self.graph.find_node_in_graph(node_id_to_search)

    def initialize_first_revision(self, first_revision):
        nodes = []
        line_number = 1
        for line_content in first_revision:
            new_node = Node('a', line_number, line_content, 1)
            nodes.append(new_node)
            line_number = line_number + 1
            self.graph.add_node(new_node, node_id=new_node.get_node_id())
        return nodes

    def slice_line(self, revision_number, line_number):
        starting_node_id = str(revision_number) + "." + str(line_number)
        starting_node = self.graph.find_node_in_graph(starting_node_id)

        slicing_dict_nodes = dict()
        slicing_dict_content_by_id = dict()

        starting_node_index = starting_node.get_node_id() + "***" + starting_node.content
        slicing_dict_content_by_id[starting_node_index] = []
        slicing_dict_nodes[starting_node] = []

        for p in self.graph.predecessors(starting_node):
            slicing_dict_nodes[p] = []
            slicing_dict_nodes[p].append(starting_node)
            p_index = p.get_node_id() + "***" + p.content
            slicing_dict_content_by_id[p_index] = []
            slicing_dict_content_by_id[p_index].append(starting_node_index)
            self.handle_predecessors(p, slicing_dict_nodes, slicing_dict_content_by_id)

        for s in self.graph.successors(starting_node):
            slicing_dict_nodes[starting_node].append(s)
            slicing_dict_nodes[s] = []
            s_index = s.get_node_id() + "***" + s.content
            slicing_dict_content_by_id[starting_node_index].append(s_index)
            slicing_dict_content_by_id[s_index] = []
            self.handle_successors(s, slicing_dict_nodes, slicing_dict_content_by_id)

        self.create_slice_subgraph(slicing_dict_nodes)

        return slicing_dict_nodes, slicing_dict_content_by_id

    def handle_successors(self, succ_node: Node, nodes_dict, content_dict):
        for s in self.graph.successors(succ_node):
            nodes_dict[succ_node].append(s)
            nodes_dict[s] = []
            s_index = s.get_node_id() + "***" + s.content
            content_dict[s_index] = []
            content_dict[succ_node.get_node_id() + "***" + succ_node.content].append(s_index)
            self.handle_successors(s, nodes_dict, content_dict)

    def handle_predecessors(self, pred_node: Node, nodes_dict, content_dict):
        for p in self.graph.predecessors(pred_node):
            nodes_dict[p] = []
            nodes_dict[p].append(pred_node)
            p_index = p.get_node_id() + "***" + p.content
            content_dict[p_index] = []
            content_dict[p_index].append(pred_node.get_node_id() + "***" + pred_node.content)
            self.handle_predecessors(p, nodes_dict, content_dict)

    def create_slice_subgraph(self, slicing_dict_nodes):
        self.sub_graph: Graph = self.graph
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

        # pos = nx.spring_layout(self.sub_graph)
        # nx.draw_networkx_nodes(self.sub_graph, pos, node_size=500)
        # nx.draw_networkx_labels(self.sub_graph, pos)
        # nx.draw_networkx_edges(self.sub_graph, pos, edge_color='r', arrows=True)
        # plt.show()
