

class Node:
    line_number: int
    content: str
    revision_number: int
    label: str

    def __init__(self, label, line_number, content, revision_number):
        self.label = label
        self.line_number = line_number
        self.content = content
        self.revision_number = revision_number

    def get_node_id(self):
        return str(self.revision_number) + "." + str(self.line_number)

    def __lt__(self, other):
        return float(self.get_node_id()) < float(other.get_node_id())
