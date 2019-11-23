from fuzzywuzzy import fuzz

from Framework.matcher import Matcher
from Framework.node import Node


class SimpleMatcher(Matcher):

    def evaluate_match(self, left_node: Node, ptr_right: int, right_lines: [str] = None):
        string_left = left_node.content
        if string_left == right_lines[ptr_right]:
            return 'u'

        # partial match
        if fuzz.partial_ratio(string_left, right_lines[ptr_right]) > 90:
            return 'c'

        return 'unmatched'
