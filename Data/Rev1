import networkx as nx
from Framework.node import Node
from fuzzywuzzy import fuzz


class GraphBuilder():

    def __init__(self):
        self.G = nx.MultiDiGraph()
        pass

    def build_graph(self, revisions):
        first_revision = revisions[0]
        starting_nodes = self.initialize_first_revision(first_revision)
        print(list(self.G.nodes(data=True)))
        beginning = starting_nodes
        for revision_number in range(1, len(revisions)):
            starting_nodes = self.build_graph_from_subsequent_revisions(starting_nodes, revisions[revision_number], revision_number)
        return beginning




    def build_graph_from_subsequent_revisions(self, left_nodes, right:[str], revision_number):
        ptr_left = 0
        ptr_right = 0
        right_nodes = []
        while True:
            left_node = left_nodes[ptr_left]
            if self.evaluate_match(left_node.content, right[ptr_right]) == 'u':
                new_right_node = Node("u", ptr_right + 1, right[ptr_right], revision_number)
                self.G.add_node(new_right_node)
                self.G.add_edge(left_node, new_right_node)
                print(list(self.G.nodes(data=True)))
                right_nodes.append(new_right_node)
                ptr_left = ptr_left + 1
                ptr_right = ptr_right + 1
                continue

            if self.evaluate_match(left_node.content, right[ptr_right]) == 'c':
                new_right_node = Node("c", ptr_right + 1, right[ptr_right], revision_number)
                self.G.add_node(new_right_node)
                self.G.add_edge(left_node, new_right_node)
                print(list(self.G.nodes(data=True)))
                right_nodes.append(new_right_node)
                ptr_right = ptr_right + 1
                continue

            #Unmatched
            if len(self.G.out_edges(self.G.nodes[left_node]["id"])) > 0:
                ptr_left = ptr_left + 1


            if ptr_left > len(left_nodes) or ptr_right > len(right):
                break
        print(list(self.G.nodes(data=True)))
        return right_nodes





    def evaluate_match(self, string_left:str, string_right):
        if string_left == string_right:
            return 'u'

        #partial match
        if fuzz.partial_ratio(string_left, string_right) > 90:
            return 'c'

        return 'unmatched'

    def initialize_first_revision(self, first_revision):
        nodes = []
        line_number = 1
        for line_content in first_revision:
            new_node = Node('a', line_number, line_content, 1)
            nodes.append(new_node)
            line_number = line_number + 1
            self.G.add_node(new_node, id = new_node.get_node_id())
        return nodes