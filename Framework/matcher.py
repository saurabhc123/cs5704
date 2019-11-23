from abc import ABC, abstractmethod

from Framework.node import Node


class Matcher(ABC):

    def evaluate_match(self, string_left: str, ptr_right, right_lines=None):
        pass