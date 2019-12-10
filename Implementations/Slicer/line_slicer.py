
from Framework.slicer import Slicer
from Framework.graph import Graph
from Framework.node import Node

class RoundFloat(float):
    def __new__(cls, value=0, places=2):
        return float.__new__(cls, value)
    def __init__(self, value=0, places=2):
        self.places = str(places)
    def __str__(self):
        return ("%." + self.places + "f") % self
    __repr__ = __str__

class LineSlicer(Slicer):

    def __init__(self, graph: Graph):
        self.G = graph


    # criterion should be starting_line, ending_line, staring_rev, ending_rev
    def slice_line(self, revision_number: int, line_number: int):
        starting_node_id = str(revision_number) + "." + str(line_number)
        starting_node = self.G.find_node_in_graph(starting_node_id)

        slicing_dict_nodes = dict()
        slicing_dict_content_by_id = dict()

        starting_node_index = starting_node.get_node_id()
        slicing_dict_content_by_id[starting_node_index] = []
        slicing_dict_nodes[starting_node] = []

        for p in self.G.predecessors(starting_node):
            slicing_dict_nodes[p] = []
            slicing_dict_nodes[p].append(starting_node)
            p_index = p.get_node_id()
            slicing_dict_content_by_id[p_index] = []
            slicing_dict_content_by_id[p_index].append(starting_node_index)
            self.handle_predecessors(p, slicing_dict_nodes, slicing_dict_content_by_id)

        for s in self.G.successors(starting_node):
            slicing_dict_nodes[starting_node].append(s)
            slicing_dict_nodes[s] = []
            s_index = s.get_node_id()
            slicing_dict_content_by_id[starting_node_index].append(s_index)
            slicing_dict_content_by_id[s_index] = []
            self.handle_successors(s, slicing_dict_nodes, slicing_dict_content_by_id)

        self.create_slice_subgraph(slicing_dict_nodes, slicing_dict_content_by_id)

        return slicing_dict_nodes, slicing_dict_content_by_id

    def handle_successors(self, succ_node: Node, nodes_dict: dict, content_dict: dict, ending_revision: int):
        for s in self.G.successors(succ_node):
            if s is not None:
                nodes_dict[succ_node].append(s)
                s_index = s.get_node_id()
                content_dict[succ_node.get_node_id()].append(s_index)
                current_revision = int(s.get_node_id().split(".")[0])
                if current_revision >= ending_revision:
                    break
                nodes_dict[s] = []
                content_dict[s_index] = []
                self.handle_successors(s, nodes_dict, content_dict, ending_revision)

    def handle_predecessors(self, pred_node: Node, nodes_dict: dict, content_dict: dict, ending_revision: int):
        for p in self.G.predecessors(pred_node):
            if p is not None:
                p_index = p.get_node_id()
                content_dict[p_index] = []
                content_dict[p_index].append(pred_node.get_node_id())
                nodes_dict[p] = []
                nodes_dict[p].append(pred_node)
                current_revision = int(p.get_node_id().split(".")[0])
                if current_revision < ending_revision:
                    break
                self.handle_predecessors(p, nodes_dict, content_dict, ending_revision)

    def create_slice_subgraph(self, slicing_dict_nodes: dict(), slicing_dict_content_by_id: dict()):
        self.sub_graph: Graph = self.G
        self.sub_graph.clear()

        nodes = list(slicing_dict_nodes.keys())
        ids = list(slicing_dict_content_by_id.keys())

        if nodes is not None:
            for n, c in zip(nodes, ids):
                if n is not None and c is not None:
                    self.sub_graph.add_node(n, node_id=c)

            for n, c in zip(nodes, ids):
                if n is not None and c is not None:
                    nodes_succs = slicing_dict_nodes[n]
                    curr_node = self.sub_graph.find_node_in_graph(c)

                if len(nodes_succs) > 0:
                    for s in nodes_succs:
                        if s is not None:
                            succ_node = self.sub_graph.find_node_in_graph(s.get_node_id())
                            if succ_node is not None:
                                self.sub_graph.add_edge(curr_node, succ_node)

    def slice(self, revision_number, line_number):
        nodes, content_id = self.slice_line(revision_number, line_number)
        self.visualize_subgraph(nodes)
        return nodes, content_id

    def visualize_subgraph(self, nodes_dict:dict):
        for i in sorted(nodes_dict.keys()):
            print(i.get_node_id())
        # keys_list = list(nodes_dict.keys())
        #
        # revision_number, line_number =

    def slice_line_updated(self, starting_revision: int, ending_revision: int, starting_line: int, ending_line: int, between: bool):
        starting_node_id = str(starting_revision) + "." + str(starting_line)
        starting_node = self.G.find_node_in_graph(starting_node_id)

        ending_node_id = str(starting_revision) + "." + str(ending_line)
        ending_node = self.G.find_node_in_graph(ending_node_id)

        slicing_dict_nodes = dict()
        slicing_dict_content_by_id = dict()

        starting_node_index = starting_node_id
        slicing_dict_content_by_id[starting_node_index] = []
        slicing_dict_nodes[starting_node] = []

        ending_node_index = ending_node_id
        slicing_dict_content_by_id[ending_node_index] = []
        slicing_dict_nodes[ending_node] = []

        if starting_node is not None and ending_node is not None:
            if (ending_revision > starting_revision):
                for s in self.G.successors(starting_node):
                    if s is not None:
                        slicing_dict_nodes[starting_node].append(s)
                        s_index = s.get_node_id()
                        slicing_dict_content_by_id[starting_node_index].append(s_index)
                        current_revision = int(s.get_node_id().split(".")[0])
                        if current_revision >= ending_revision:
                            break
                        slicing_dict_nodes[s] = []
                        slicing_dict_content_by_id[s_index] = []
                        self.handle_successors(s, slicing_dict_nodes, slicing_dict_content_by_id, ending_revision)

                for s in self.G.successors(ending_node):
                    if s is not None:
                        slicing_dict_nodes[ending_node].append(s)
                        s_index = s.get_node_id()
                        slicing_dict_content_by_id[ending_node_index].append(s_index)
                        current_revision = int(s.get_node_id().split(".")[0])
                        if current_revision >= ending_revision:
                            break
                        slicing_dict_nodes[s] = []
                        slicing_dict_content_by_id[s_index] = []
                        self.handle_successors(s, slicing_dict_nodes, slicing_dict_content_by_id, ending_revision)

                if between is True:
                    direct_successors = []
                    starting_slice_current_nodes = slicing_dict_content_by_id[starting_node_index]
                    ending_slicing_current_nodes = slicing_dict_content_by_id[ending_node_index]
                    for s in starting_slice_current_nodes:
                        direct_successors.append(s)
                    for s in ending_slicing_current_nodes:
                        if s not in direct_successors:
                            direct_successors.append(s)
                    direct_successors.sort()
                    if len(direct_successors) > 0:
                        first_line_number = direct_successors[0].split(".")[1]
                        first_node = float(direct_successors[0])
                        last_node = float(direct_successors[len(direct_successors) - 1])
                        i = RoundFloat(first_node + pow(0.1, len(first_line_number)), places=len(first_line_number)) # NEED TO FIX FOR TRAILING 0s
                        while i < last_node:
                            found = False
                            node_index = None
                            for k in slicing_dict_content_by_id.keys():
                                if str(i) == k:
                                    found = True
                                    break
                            if found is False:
                                curr_node_index = str(i)
                                node_index = self.G.find_node_in_graph(curr_node_index)
                                slicing_dict_content_by_id[curr_node_index] = []
                                if node_index is not None:
                                    slicing_dict_nodes[node_index] = []
                            i = RoundFloat(i + pow(0.1, len(first_line_number)), places=len(first_line_number))
                        self.handle_between(direct_successors, slicing_dict_content_by_id, slicing_dict_nodes)
            else:
                for p in self.G.predecessors(starting_node):
                    if p is not None:
                        slicing_dict_nodes[p] = []
                        slicing_dict_nodes[p].append(starting_node)
                        p_index = p.get_node_id()
                        slicing_dict_content_by_id[p_index] = []
                        slicing_dict_content_by_id[p_index].append(starting_node_index)
                        current_revision = int(p.get_node_id().split(".")[0])
                        if current_revision <= ending_revision:
                            break
                        self.handle_predecessors(p, slicing_dict_nodes, slicing_dict_content_by_id, ending_revision)

                for p in self.G.predecessors(ending_node):
                    if p is not None:
                        slicing_dict_nodes[p] = []
                        slicing_dict_nodes[p].append(ending_node)
                        p_index = p.get_node_id()
                        slicing_dict_content_by_id[p_index] = []
                        slicing_dict_content_by_id[p_index].append(ending_node_index)
                        current_revision = int(p.get_node_id().split(".")[0])
                        if current_revision <= ending_revision:
                            break
                        self.handle_predecessors(p, slicing_dict_nodes, slicing_dict_content_by_id, ending_revision)

                if between is True:
                    between_nodes = []
                    for k in slicing_dict_content_by_id.keys():
                        rev_number = k.split(".")[0]
                        if int(rev_number) == ending_revision:
                            curr_nodes = slicing_dict_content_by_id[k]
                            for n in curr_nodes:
                                between_nodes.append(n)
                    between_nodes.sort()
                    if len(between_nodes) > 0:
                        first_line_number = between_nodes[0].split(".")[1]
                        first_node = float(between_nodes[0])
                        last_node = float(between_nodes[len(between_nodes) - 1])
                        i = RoundFloat(first_node + pow(0.1, len(first_line_number)), places=len(first_line_number))
                        while i < last_node:
                            found = False
                            node_index = None
                            for k in slicing_dict_content_by_id.keys():
                                if str(i) == k:
                                    found = True
                                    break
                            if found is False:
                                curr_node_index = str(i)
                                node_index = self.G.find_node_in_graph(curr_node_index)
                                slicing_dict_content_by_id[curr_node_index] = []
                                if node_index is not None:
                                    slicing_dict_nodes[node_index] = []
                            i = RoundFloat(i + pow(0.1, len(first_line_number)), places=len(first_line_number))
                        self.handle_between(between_nodes, slicing_dict_content_by_id, slicing_dict_nodes)

            arranged_slices = self.arrange_slices(slicing_dict_content_by_id)
            self.create_slice_subgraph(slicing_dict_nodes, slicing_dict_content_by_id)

            return slicing_dict_nodes, slicing_dict_content_by_id, arranged_slices
        return None, None, None

    def slice_updated(self, starting_revision: int, ending_revision: int, starting_line: int, ending_line: int,
                      between: bool):
        nodes, content_id, arranged_slices = self.slice_line_updated(starting_revision, ending_revision, starting_line, ending_line, between)
        return nodes, content_id, arranged_slices

    def handle_between(self, successors: [str], slicing_dict_content_by_id: dict(), slicing_dict_nodes: dict()):
        direct_successors = []
        for succ in successors:
            if succ in slicing_dict_content_by_id.keys():
                succ_succ = slicing_dict_content_by_id[succ]
                for s in succ_succ:
                    direct_successors.append(s)
        direct_successors.sort()
        if len(direct_successors) > 0:
            first_line_number = direct_successors[0].split(".")[1]
            # last_line_number = direct_successors[len(direct_successors) - 1].split(".")[1]
            first_node = float(direct_successors[0])
            last_node = float(direct_successors[len(direct_successors) - 1])
            i = RoundFloat(first_node + pow(0.1, len(first_line_number)), places=len(first_line_number))
            while i < last_node:
                found = False
                node_index = None
                for k in slicing_dict_content_by_id.keys():
                    if str(i) == k:
                        found = True
                        break
                if found is False:
                    curr_node_index = str(i)
                    node_index = self.G.find_node_in_graph(curr_node_index)
                    slicing_dict_content_by_id[curr_node_index] = []
                    if node_index is not None:
                        slicing_dict_nodes[node_index] = []
                i = RoundFloat(i + pow(0.1, len(first_line_number)), places=len(first_line_number))
        if len(direct_successors) > 0:
            self.handle_between(direct_successors, slicing_dict_content_by_id, slicing_dict_nodes)

    def arrange_slices(self, slicing_dict_content_by_id: dict()):
        keys = sorted(slicing_dict_content_by_id)
        curr_revision_number_set = keys[0].split(".")[0]
        index = 0
        revisions = [[]]
        for k in keys:
            rev_number = k.split(".")[0]
            if rev_number == curr_revision_number_set:
                revisions[index].append(k)
                continue
            elif rev_number > curr_revision_number_set:
                revisions.append([])
                index = index + 1
                revisions[index].append(k)
                curr_revision_number_set = rev_number
        return revisions