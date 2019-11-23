from Framework.matcher import Matcher
from Framework.node import Node


class DeserializationMatcher(Matcher):

    def __init__(self, edge_tuples):
        self.edge_tuples = edge_tuples
        self.revision_tuples = {}
        self.parse_tuples()

    def evaluate_match(self, left_node: Node, ptr_right: int, right_lines: [str] = None):
        tuple_id = "Rev" + str(left_node.revision_number)
        revision_edges = self.revision_tuples[tuple_id]
        for i in range(revision_edges):
            edge_tuple = revision_edges[i]
            left_line_number = edge_tuple[0]
            right_line_number = edge_tuple[2]
            edge_label = edge_tuple[1]
            if left_node.line_number == left_line_number and ptr_right == right_line_number:
                return edge_label

        return 'unmatched'

    def parse_tuples(self):
        # Parse the tuples based on the header.
        # Create a dictionary based on the left revision ID.
        left_revision_id:str = None
        for edge_tuple in self.edge_tuples:
            # If header
            if len(edge_tuple) == 2:
                left_revision_id = edge_tuple[0]
                self.revision_tuples[left_revision_id] = []
                continue
            # Content
            left_line_number = edge_tuple[0]
            right_line_number = edge_tuple[2]
            label = edge_tuple[1]
            self.revision_tuples[left_revision_id].append((left_line_number, label, right_line_number))
