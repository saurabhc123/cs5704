from Framework.serializer import Serializer


class CsvFileSerializer(Serializer):

    def __init__(self, folder, file_name):
        self.file_name = file_name
        self.folder = folder
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


    def deserialize(self, output_data_bag):
        pass

    def write_header(self, left_revision_string, right_revision_string):
        pass

    def write_edge(self, line_number, param, line_number1):
        pass