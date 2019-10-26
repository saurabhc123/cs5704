import networkx as nx
import Framework.graph_builder as gb




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

    assert beginning[4].label == "d"
    assert beginning[8].label == "u"
    assert beginning[9].label == "a"


