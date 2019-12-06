import Implementations.GraphBuilder.simple_graph_builder as gb
from Framework.Matchers.simple_matcher import SimpleMatcher

rev1 = [
    "a",
    "b.1",
    "b.2",
    "c",
    "b.3"
]

# rev2 = [
#     "a",
#     "b.1",
#     "b.2",
#     "e.1"
# ]

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

def test1():
    rev1 = [
        "a",
        "b.1",
        "b.2",
        "c",
        "b.3"
    ]

    # rev2 = [
    #     "a",
    #     "b.1",
    #     "b.2",
    #     "e.1"
    # ]

    rev2 = [
        "a",
        "b.1",
        "b.2",
        "b.3",
        "c"
    ]

    revisions = [rev1, rev2]
    simple_matcher = SimpleMatcher()
    gb_obj = gb.SimpleGraphBuilder(simple_matcher)
    beginning = gb_obj.build_graph(revisions)

    assert beginning[3].label == "u"
    assert beginning[4].label == "a"

def test2():
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
    simple_matcher = SimpleMatcher()
    gb_obj = gb.SimpleGraphBuilder(simple_matcher)
    beginning = gb_obj.build_graph(revisions)

    assert beginning[0].label == "u"
    assert beginning[1].label == "c"
    assert beginning[2].label == "c"
    assert beginning[3].label == "u"
    assert beginning[4].label == "u"
    assert beginning[5].label == "c"


test1()
test2()







