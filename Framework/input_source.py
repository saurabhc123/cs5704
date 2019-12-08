from abc import ABC, abstractmethod

from Framework.node import Node


class InputSource(ABC):

    def get_files_with_revisions(self, input_source):
        pass