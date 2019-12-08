from abc import ABC, abstractmethod


class Visualizer(ABC):

    def visualize(self, arranged_slices, revisions, forwards = True):
        pass