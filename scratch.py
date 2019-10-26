import networkx as nx
import Framework.graph_builder as gb



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
    gb_obj = gb.GraphBuilder()
    beginning = gb_obj.build_graph(revisions)

    assert beginning[3].label == "u"
    assert beginning[4].label == "a"

test1()







