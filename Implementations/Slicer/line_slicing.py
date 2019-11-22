
from Framework.slicer import Slicer
from Framework.graph import Graph


class LineSlicing(Slicer):

    def slice(self, revision_number: int, line_number: int):
        starting_node_id = str.join(str(self.revision_number) + ".", str(self.line_number))
        starting_node = self.Graph.find_node_in_graph(starting_node_id)




