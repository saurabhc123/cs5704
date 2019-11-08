
from abc import ABC, abstractmethod

from Framework.node import Node


class Serializer(ABC):

    def serialize(self, edge_list):
        pass

    def deserialize(self, output_data_bag):
        pass