from Framework.serializer import Serializer


class InMemorySerializer(Serializer):

    def __init__(self):
        self.edges = []
        pass

    def serialize(self, edge_list):
        left_revision_number = edge_list[0][0].revision_number
        left_revision_string = "Rev" + str(left_revision_number)
        right_revision_number = edge_list[0][1].revision_number
        right_revision_string = "Rev" + str(right_revision_number)
        self.write_header(left_revision_string, right_revision_string)

        for i in range(len(edge_list)):
            if left_revision_number != edge_list[i][0].revision_number:
                left_revision_number = edge_list[i][0].revision_number
                left_revision_string = "Rev" + str(left_revision_number)
                right_revision_number = edge_list[i][1].revision_number
                right_revision_string = "Rev" + str(right_revision_number)
                self.write_header(left_revision_string, right_revision_string)
            self.write_edge(edge_list[i][0].line_number, edge_list[i][2], edge_list[i][1].line_number)

    def write_header(self, left_revision_string, right_revision_string):
        self.edges.append("{},{}".format(left_revision_string, right_revision_string))

    def write_edge(self, left_line_number, label, right_line_number):
        self.edges.append("{},{},{}".format(left_line_number, label, right_line_number))

    def deserialize(self, output_data_bag):
        edges = self.edges
        revision_number = 0
        mappings = []
        revision_mappings = {}
        for line in edges:
            if self.does_line_contain_revision_info(line):
                revision_number = revision_number + 1
                revision_mappings = {}
                mappings.append(revision_mappings)
                continue
            (left_line_number, label, right_line_number) = self.get_edge_info_from_line(line)
            if left_line_number not in revision_mappings:
                mappings[revision_number - 1][left_line_number] = {}
            mappings[revision_number - 1][left_line_number][right_line_number] = label

        return mappings

    def does_line_contain_revision_info(self, line):
        if "Rev" in line:
            return True
        return False

    def get_edge_info_from_line(self, line):
        line_info = line.split(',')
        return int(line_info[0]), line_info[1], int(line_info[2])