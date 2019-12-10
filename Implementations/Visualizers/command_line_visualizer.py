from Framework.Visualizer import Visualizer


class CommandLineVisualizer(Visualizer):

    def visualize(self, arranged_slices, nodes, content_ids, revisions, forwards = True):
        nodes_dict = dict()
        for arr in arranged_slices:
            if len(arr) > 0:
                for c in arr:
                    for n, ci in zip(nodes, content_ids):
                        if c == ci:
                            nodes_dict[c] = n

        if forwards is True:
            for arr in arranged_slices:
                if len(arr) > 0:
                    print("-----------------------------Revision ", arr[0].split(".")[0], "-----------------------------")
                    print()
                    for c in arr:
                        rev_index = int(c.split(".")[0]) - 1
                        line_index = int(c.split(".")[1]) - 1
                        if nodes_dict[c].label == 'a':
                            print(revisions[rev_index][line_index], "+++")
                        elif nodes_dict[c].label == 'd':
                            print(revisions[rev_index][line_index], "---")
                        else:
                            print(revisions[rev_index][line_index])
                    print()
        else:
            for arr in reversed(arranged_slices):
                if len(arr) > 0:
                    print("-----------------------------Revision ", arr[0].split(".")[0], "-----------------------------")
                    print()
                    for c in arr:
                        rev_index = int(c.split(".")[0]) - 1
                        line_index = int(c.split(".")[1]) - 1
                        if nodes_dict[c].label == 'a':
                            print(revisions[rev_index][line_index], "+++")
                        elif nodes_dict[c].label == 'd':
                            print(revisions[rev_index][line_index], "---")
                        else:
                            print(revisions[rev_index][line_index])
                    print()
