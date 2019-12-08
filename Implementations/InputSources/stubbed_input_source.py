from Framework.input_source import InputSource


class StubbedInputSource(InputSource):

    def __init__(self, revisions=None):
        self.revisions = revisions

    def get_files_with_revisions(self, input_source=None):
        return self.revisions
