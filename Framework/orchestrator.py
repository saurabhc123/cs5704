from Framework import Visualizer
from Framework.graph import Graph
from Framework.graph_builder import GraphBuilder
from Framework.input_source import InputSource
from Framework.mapper import Mapper
from Framework.slicer import Slicer
from Implementations.Graphs.networkx_graph import NetworkxGraph
from Implementations.Serializers.in_memory_serializer import InMemorySerializer
import Implementations.GraphBuilder.simple_graph_builder as gb


class Orchestrator:

    def __init__(self,
                 input_source: InputSource,
                 mapper: Mapper,
                 graph: Graph,
                 slicer: Slicer,
                 visualizer:Visualizer = None):
        self.input_source = input_source
        self.mapper = mapper
        self.graph = graph
        self.slicer = slicer
        self.revisions:[] = None
        self.visualizer = visualizer

    def orchestrate(self):

        # Get file contents for each revision for a single file
        file_revisions = self.input_source.get_files_with_revisions()
        self.revisions = file_revisions
        # Initialize Mappings
        self.mapper.initialize_mappings(file_revisions)
        gb_obj = gb.SimpleGraphBuilder(self.mapper, self.graph)
        beginning = gb_obj.build_graph(file_revisions)
        gb_obj.graph.serialize_graph()
        return beginning

    def get_revisions(self):
        return self.revisions

    def visualize(self, arranged_slices, nodes, content_ids, forwards = True):
        if arranged_slices is not None:
            self.visualizer.visualize(arranged_slices, nodes, content_ids, self.revisions, forwards)

    def slice(self, revision_number, line_number):
        return self.slicer.slice(revision_number, line_number)

    def slice_updated(self, starting_revision: int, ending_revision: int, starting_line: int, ending_line: int, between: bool):
        return self.slicer.slice_updated(starting_revision, ending_revision, starting_line, ending_line, between)
