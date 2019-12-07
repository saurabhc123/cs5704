from fuzzywuzzy import fuzz

from Framework.Matchers.simple_matcher import SimpleMatcher
from Framework.input_source import InputSource
from Framework.mapper import Mapper
from Framework.node import Node


class SimpleMapper(Mapper):

    def __init__(self, mappings=None):
        self.matcher = SimpleMatcher()
        self.revisions = None
        self.mappings = mappings
        pass

    def initialize_mappings(self, revisions):
        self.revisions = revisions
        if self.mappings is None:
            self.mappings = []
            self.build_graph(self.revisions)

    def get_mapping(self, left_line_number: int, right_line_number: int, left_revision_number):
        if self.mappings[left_revision_number - 1] is not None:
            if left_line_number in self.mappings[left_revision_number - 1]:
                if right_line_number in self.mappings[left_revision_number - 1][left_line_number]:
                    return self.mappings[left_revision_number - 1][left_line_number][right_line_number]

        return "unmatched"

    def build_graph(self, revisions):
        first_revision = revisions[0]
        starting_nodes = self.initialize_first_revision(first_revision)
        history_graph = [starting_nodes]
        for revision_number in range(1, len(revisions)):
            self.mappings.append({})
            starting_nodes = self.build_graph_from_subsequent_revisions(starting_nodes, revisions[revision_number],
                                                                        revision_number)
            history_graph.append(starting_nodes)
        return history_graph

    def build_graph_from_subsequent_revisions(self, left_nodes, right: [str], revision_number):
        ptr_left = 0
        ptr_right = 0
        right_nodes = []
        current_revision_mappings: {} = self.mappings[revision_number - 1]
        while True:
            # if no more to process on the right side and the left side
            if ptr_left >= len(left_nodes) and ptr_right >= len(right):
                break

            # if no more to process on the left side, but more on the right side
            if ptr_left >= len(left_nodes) and ptr_right < len(right):
                for i in range(ptr_right, len(right)):
                    new_right_node = Node("a", ptr_right + 1, right[ptr_right], revision_number + 1)
                    right_nodes.append(new_right_node)
                break

            # If more to process on the left side and no more to process on the right side,
            if ptr_left < len(left_nodes) and ptr_right >= len(right):
                break

            left_node = left_nodes[ptr_left]
            match_result = self.matcher.evaluate_match(left_node.content, right[ptr_right])
            if match_result == 'u':
                if ptr_left + 1 not in current_revision_mappings:
                    current_revision_mappings[ptr_left + 1] = {}
                current_revision_mappings[ptr_left + 1][ptr_right + 1] = match_result
                new_right_node = Node(match_result, ptr_right + 1, right[ptr_right], revision_number + 1)
                right_nodes.append(new_right_node)
                ptr_left = ptr_left + 1
                ptr_right = ptr_right + 1
                continue

            match_result = self.matcher.evaluate_match(left_node.content, right[ptr_right])
            if match_result == 'c':
                if ptr_left + 1 not in current_revision_mappings:
                    current_revision_mappings[ptr_left + 1] = {}
                current_revision_mappings[ptr_left + 1][ptr_right + 1] = match_result
                new_right_node = Node(match_result, ptr_right + 1, right[ptr_right], revision_number + 1)
                right_nodes.append(new_right_node)
                ptr_right = ptr_right + 1
                continue

                # Unmatched
            if ptr_left + 1 in current_revision_mappings:
                ptr_left = ptr_left + 1
                continue

            ptr_left, ptr_right = self.handle_unmatched(ptr_left, ptr_right, left_nodes, right, right_nodes)

        return right_nodes

    def handle_unmatched(self, ptr_left: int, ptr_right: int, left_nodes: [Node], right, right_nodes: [Node]):
        left_revision_number = left_nodes[ptr_left].revision_number
        right_revision_number = left_revision_number + 1
        current_revision_mappings: {} = self.mappings[left_revision_number - 1]
        # Increment the left ptr
        ptr_left = ptr_left + 1
        # If left_ptr out of bounds
        if ptr_left >= len(left_nodes):
            ptr_left = ptr_left - 1
            new_right_node = Node("a", ptr_right + 1, right[ptr_right], left_revision_number + 1)
            right_nodes.append(new_right_node)
            ptr_right = ptr_right + 1
            return ptr_left, ptr_right
        # Compare left_ptr and right
        left_node = left_nodes[ptr_left]
        match_result = self.matcher.evaluate_match(left_node.content, right[ptr_right])
        if "unmatched" in match_result:
            new_right_node = Node("a", ptr_right + 1, right[ptr_right], left_revision_number + 1)
            right_nodes.append(new_right_node)
            ptr_right = ptr_right + 1
            ptr_left = ptr_left - 1
            return ptr_left, ptr_right
        else:
            if ptr_left + 1 not in current_revision_mappings:
                current_revision_mappings[ptr_left + 1] = {}
            current_revision_mappings[ptr_left + 1][ptr_right + 1] = match_result
            # Increment left_ptr and right_ptr by 1
            new_right_node = Node(match_result, ptr_right + 1, right[ptr_right], left_revision_number + 1)
            right_nodes.append(new_right_node)
            ptr_right = ptr_right + 1
            ptr_left = ptr_left + 1
            return ptr_left, ptr_right

    # def get_node_from_graph(self, left_nodes, ptr_left):
    #     node_id_to_search = left_nodes[ptr_left].get_node_id()
    #     return self.graph.find_node_in_graph(node_id_to_search)
    #

    def initialize_first_revision(self, first_revision):
        nodes = []
        line_number = 1
        for line_content in first_revision:
            new_node = Node('a', line_number, line_content, 1)
            nodes.append(new_node)
            line_number = line_number + 1
            # self.graph.add_node(new_node, node_id=new_node.get_node_id())
        return nodes
