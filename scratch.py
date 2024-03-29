import Implementations.GraphBuilder.simple_graph_builder as gb
from Framework.Matchers.simple_matcher import SimpleMatcher
from Implementations.Graphs.networkx_graph import NetworkxGraph

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

rev3 = [
    "a.1",
    "b.1",
    "b.2",
    "b.3",
    "d",
    "e.1",
    "e.2"
]

rev4 = [
    "b.1",
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
    networkx_graph = NetworkxGraph()
    simple_matcher = SimpleMatcher()
    gb_obj = gb.SimpleGraphBuilder(simple_matcher)
    beginning = gb_obj.build_graph(revisions)

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
    networkx_graph = NetworkxGraph()
    simple_matcher = SimpleMatcher()
    gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph)
    beginning = gb_obj.build_graph(revisions)
    gb_obj.slice_line(1, 2)

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
    networkx_graph = NetworkxGraph()
    simple_matcher = SimpleMatcher()
    gb_obj = gb.SimpleGraphBuilder(simple_matcher)
    beginning = gb_obj.build_graph(revisions)

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
    networkx_graph = NetworkxGraph()
    simple_matcher = SimpleMatcher()
    gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph)
    beginning = gb_obj.build_graph(revisions)

    assert beginning[0][1].label == "a"
    assert beginning[0][2].label == "a"
    assert beginning[0][3].label == "d"
    assert beginning[0][4].label == "d"
    assert beginning[0][5].label == "d"
    assert beginning[0][6].label == "d"
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
    networkx_graph = NetworkxGraph()
    simple_matcher = SimpleMatcher()
    gb_obj = gb.GraphBuilder(simple_matcher, networkx_graph)
    beginning = gb_obj.build_graph(revisions)
    gb_obj.slice_line(1, 1)
    print(beginning[1][1].content)


test_with_actual_files()
# test_check_displacement()
# test_mutation_of_lines()
# test_right_addition()
# test_blanks()







