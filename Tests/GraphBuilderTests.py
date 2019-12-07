import Implementations.GraphBuilder.old_graph_builder as gb
from Framework.Matchers.simple_matcher import SimpleMatcher
from Framework.orchestrator import Orchestrator
from Implementations.Graphs.networkx_graph import NetworkxGraph
from Implementations.Serializers.csv_file_serializer import CsvFileSerializer
from Implementations.Slicer.line_slicer import LineSlicer
from Implementations.InputSources.stubbed_input_source import StubbedInputSource
from Implementations.Mappers.simple_mapper import SimpleMapper
from Implementations.Serializers.in_memory_serializer import InMemorySerializer
import os
import git
from git import Repo

rev1 = [
    "a",
    "b",
    "c",
]

rev2 = [
    "a",
    "b.1",
    "b.2",
    "c",
    "b.3"
]

rev3 = [
    "a",
    "b.1",
    "b.2",
    "b.3",
    "c"
]

rev4 = [
    "a.1",
    "b.1",
    "b.2",
    "b.3",
    "d",
    "e.1",
    "e.2"
]

rev5 = [
    "b.1.1",
    "b.1.2",
    "b.2",
    "d",
    "e.2"
]


# def main():
#     # revisions = [rev1, rev2, rev3, rev4]
#     revisions = [rev1, rev2]
#     gb_obj = gb.GraphBuilder()
#     beginning = gb_obj.build_graph(revisions)
#
# main()


def large_test():
    revisions = [rev1, rev2, rev3, rev4, rev5]
    # networkx_graph = NetworkxGraph()
    # simple_matcher = SimpleMatcher()
    # slicer = LineSlicing(networkx_graph)
    # gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph, slicer)
    # beginning = gb_obj.build_graph(revisions)
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    print(beginning[1][1].content)
    slicing_dict, slicing_dict_content = orchestrator.slice(2, 2)
    print(slicing_dict)
    print(slicing_dict_content)


def test_check_displacement():
    rev1 = [
        "a",
        "b.1",
        "b.2",
        "c",
        "b.3"
    ]

    rev2 = [
        "a",
        "b.1",
        "b.2",
        "b.3",
        "c"
    ]

    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    assert beginning[1][3].label == "u"
    assert beginning[1][4].label == "a"


def test_mutation_of_lines():
    rev1 = [
        "a",
        "b",
        "c",
        "d",
        "e"
    ]

    rev2 = [
        "a",
        "b.1",
        "b.2",
        "c",
        "d",
        "e.1"
    ]
    beginning = None
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    assert beginning[1][0].label == "u"
    assert beginning[1][1].label == "c"
    assert beginning[1][2].label == "c"
    assert beginning[1][3].label == "u"
    assert beginning[1][4].label == "u"
    assert beginning[1][5].label == "c"


def test_right_addition():
    rev1 = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "",
        "",
        "",
        "",
        "",
        "fd"
    ]

    rev2 = [
        "a",
        "b",
        "f",
        "c",
        "d",
        "e",
        "",
        "",
        "yz"
    ]
    beginning = None
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    assert beginning[0][2].label == "a"
    assert beginning[1][2].label == "a"
    assert beginning[1][3].label == "u"
    assert beginning[1][3].content == rev1[2]
    assert beginning[1][4].label == "u"
    assert beginning[1][5].label == "u"


def test_blanks():
    rev1 = [
        "e",
        "",
        "",
        "",
        "",
        "",
        "fd"
    ]

    rev2 = [
        "e",
        "",
        "",
        "yz"
    ]
    beginning = None
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    assert beginning[0][1].label == "a"
    assert beginning[0][2].label == "a"
    assert beginning[0][3].label == "d"
    # assert beginning[0][4].label == "d"
    # assert beginning[0][5].label == "d"
    # assert beginning[0][6].label == "d"
    assert beginning[1][1].label == "u"
    assert beginning[1][2].label == "u"
    assert beginning[1][3].label == "a"


def ReadTextFromFile(file_name):
    f = open(file_name, "r")
    return f.read().split('\n')


def test_with_actual_files():
    rev1 = ReadTextFromFile("Data/Rev1")
    rev2 = ReadTextFromFile("Data/Rev2")
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()


def test_multiple_files():
    rev1 = ReadTextFromFile("Data/dummy_test_rev1.txt")
    rev2 = ReadTextFromFile("Data/dummy_test_rev2.txt")
    rev3 = ReadTextFromFile("Data/dummy_test_rev3.txt")
    rev4 = ReadTextFromFile("Data/dummy_test_rev4.txt")
    revisions = [rev1, rev2, rev3, rev4]
    # networkx_graph = NetworkxGraph()
    # simple_matcher = SimpleMatcher()
    # gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph)
    # beginning = gb_obj.build_graph(revisions)
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()
    print(beginning[2][4].label)
    nodes, content = orchestrator.slice(3, 5)
    print(content)


def test_serialization():
    rev1 = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "fd",
        "z"
    ]

    rev2 = [
        "a",
        "x",
        "c",
        "e",
        "y",
        "z.1"
    ]
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()
    assert beginning[1][0].label == "u"
    assert beginning[1][2].label == "u"
    assert beginning[1][3].label == "u"
    assert beginning[1][5].label == "c"


def test_deserialization():
    rev1 = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "fd",
        "z"
    ]

    rev2 = [
        "a",
        "x",
        "c",
        "e",
        "y",
        "z.1"
    ]
    revisions = [rev1, rev2]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    csv_serializer = CsvFileSerializer("Data", "deserizalized.csv")
    networkx_graph = NetworkxGraph(csv_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()
    assert beginning[1][0].label == "u"
    assert beginning[1][2].label == "u"
    assert beginning[1][3].label == "u"
    assert beginning[1][5].label == "c"


def test_multiple_file_deserialization():
    rev1 = ReadTextFromFile("Data/dummy_test_rev1.txt")
    rev2 = ReadTextFromFile("Data/dummy_test_rev2.txt")
    rev3 = ReadTextFromFile("Data/dummy_test_rev3.txt")
    rev4 = ReadTextFromFile("Data/dummy_test_rev4.txt")
    revisions = [rev1, rev2, rev3, rev4]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    # csv_serializer = CsvFileSerializer("Data", "multi_line.csv")
    # networkx_graph = NetworkxGraph(csv_serializer)
    in_memory_serializer = InMemorySerializer()
    networkx_graph = NetworkxGraph(in_memory_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()
    mappings = in_memory_serializer.deserialize(None)
    assert mapper.get_mapping(1, 1, 1) == mappings[0][1][1]
    assert mapper.get_mapping(2, 2, 1) == mappings[0][2][2]
    assert mapper.get_mapping(8, 8, 1) == mappings[0][8][8]

    assert mapper.get_mapping(1, 1, 2) == mappings[1][1][1]
    assert mapper.get_mapping(5, 7, 2) == mappings[1][5][7]
    assert mapper.get_mapping(6, 8, 2) == mappings[1][6][8]

    assert mapper.get_mapping(1, 1, 3) == mappings[2][1][1]
    assert mapper.get_mapping(3, 7, 3) == mappings[2][3][7]
    assert mapper.get_mapping(4, 8, 3) == mappings[2][4][8]

def test_multiple_file_csv_deserialization():
    rev1 = ReadTextFromFile("Data/dummy_test_rev1.txt")
    rev2 = ReadTextFromFile("Data/dummy_test_rev2.txt")
    rev3 = ReadTextFromFile("Data/dummy_test_rev3.txt")
    rev4 = ReadTextFromFile("Data/dummy_test_rev4.txt")
    revisions = [rev1, rev2, rev3, rev4]
    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    csv_serializer = CsvFileSerializer("Data", "multi_line.csv")
    networkx_graph = NetworkxGraph(csv_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()
    mappings = csv_serializer.deserialize(os.path.join("Data", "multi_line.csv"))
    assert mapper.get_mapping(1, 1, 1) == mappings[0][1][1]
    assert mapper.get_mapping(2, 2, 1) == mappings[0][2][2]
    assert mapper.get_mapping(8, 8, 1) == mappings[0][8][8]

    assert mapper.get_mapping(1, 1, 2) == mappings[1][1][1]
    assert mapper.get_mapping(5, 7, 2) == mappings[1][5][7]
    assert mapper.get_mapping(6, 8, 2) == mappings[1][6][8]

    assert mapper.get_mapping(1, 1, 3) == mappings[2][1][1]
    assert mapper.get_mapping(3, 7, 3) == mappings[2][3][7]
    assert mapper.get_mapping(4, 8, 3) == mappings[2][4][8]

def test_graph_building_via_deserialization():
    rev1 = ReadTextFromFile("Data/dummy_test_rev1.txt")
    rev2 = ReadTextFromFile("Data/dummy_test_rev2.txt")
    rev3 = ReadTextFromFile("Data/dummy_test_rev3.txt")
    rev4 = ReadTextFromFile("Data/dummy_test_rev4.txt")
    revisions = [rev1, rev2, rev3, rev4]
    input_source = StubbedInputSource(revisions)

    csv_serializer = CsvFileSerializer("Data", "multi_line.csv")
    serializer = InMemorySerializer()
    mappings = csv_serializer.deserialize(os.path.join("Data", "multi_line.csv"))
    mapper = SimpleMapper(mappings)
    networkx_graph = NetworkxGraph(serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()

    assert mapper.get_mapping(1, 1, 1) == mappings[0][1][1]
    assert mapper.get_mapping(2, 2, 1) == mappings[0][2][2]
    assert mapper.get_mapping(8, 8, 1) == mappings[0][8][8]

    assert mapper.get_mapping(1, 1, 2) == mappings[1][1][1]
    assert mapper.get_mapping(5, 7, 2) == mappings[1][5][7]
    assert mapper.get_mapping(6, 8, 2) == mappings[1][6][8]

    assert mapper.get_mapping(1, 1, 3) == mappings[2][1][1]
    assert mapper.get_mapping(3, 7, 3) == mappings[2][3][7]
    assert mapper.get_mapping(4, 8, 3) == mappings[2][4][8]

def test_git_files_as_input():

    bare_repo = Repo("./")
    assert bare_repo
    path = "Framework/orchestrator.py"
    relevant_commits = list(bare_repo.iter_commits(paths=path))

    revlist = (
        (commit, (commit.tree / path).data_stream.read())
        for commit in relevant_commits
    )

    revisions = []
    for commit, filecontents in revlist:
        str_file_contents = str(filecontents).split("\\n")
        revisions.append(str_file_contents)

    input_source = StubbedInputSource(revisions)
    mapper = SimpleMapper()
    csv_serializer = CsvFileSerializer("Data", "actual_code.csv")
    networkx_graph = NetworkxGraph(csv_serializer)
    slicer = LineSlicer(networkx_graph)
    orchestrator = Orchestrator(input_source, mapper, networkx_graph, slicer)
    beginning = orchestrator.orchestrate()


test_git_files_as_input()
test_graph_building_via_deserialization()
test_multiple_file_csv_deserialization()
test_multiple_file_deserialization()
test_deserialization()
test_with_actual_files()
test_check_displacement()
test_mutation_of_lines()
test_serialization()
test_right_addition()
test_blanks()
large_test()
test_multiple_files()
