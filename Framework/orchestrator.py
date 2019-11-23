from Framework.Matchers.simple_matcher import SimpleMatcher
from Framework.input_source import InputSource
from Framework.mapper import Mapper
from Implementations.Graphs.networkx_graph import NetworkxGraph
from Implementations.Serializers.in_memory_serializer import InMemorySerializer
import Framework.graph_builder as gb


class Orchestrator:

    def __init__(self,
                 input_source: InputSource,
                 mapper: Mapper):
        self.input_source = input_source
        self.mapper = mapper

    def orchestrate(self):

        # Get file contents for each revision for a single file
        file_revisions = self.input_source.get_files_with_revisions()

        # Initialize Mappings
        self.mapper.initialize_mappings(file_revisions)

        # in_memory_serializer = InMemorySerializer()
        # networkx_graph = NetworkxGraph(in_memory_serializer)
        # simple_matcher = SimpleMatcher()
        # gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph)
        # beginning = gb_obj.build_graph(revisions)
        # gb_obj.graph.serialize_graph()