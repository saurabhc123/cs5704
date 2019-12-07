import os
import pickle

from Framework.serializer import Serializer


class CsvFileSerializer(Serializer):

    def __init__(self, folder, file_name):
        self.file_name = file_name
        self.folder = folder
        self.buffer = []
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

        full_file_path = os.path.join(self.folder, self.file_name)
        with open(full_file_path, 'w') as filehandle:
            filehandle.writelines("%s\n" % line for line in self.buffer)

    def deserialize(self, output_data_bag):
        pass

    def write_header(self, left_revision_string, right_revision_string):
        self.buffer.append("{},{}".format(left_revision_string, right_revision_string))

    def write_edge(self, left_line_number, param, right_line_number):
        self.buffer.append("{},{},{}".format(left_line_number, param, right_line_number))
