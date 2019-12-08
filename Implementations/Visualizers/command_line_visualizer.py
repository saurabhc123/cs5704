from Framework.Visualizer import Visualizer


class CommandLineVisualizer(Visualizer):

    def visualize(self, arranged_slices, revisions, forwards = True):
        if forwards is True:
            for arr in arranged_slices:
                print("Revision ", arr[0].split(".")[0])
                for c in arr:
                    rev_index = int(c.split(".")[0]) - 1
                    line_index = int(c.split(".")[1]) - 1
                    print(revisions[rev_index][line_index])
