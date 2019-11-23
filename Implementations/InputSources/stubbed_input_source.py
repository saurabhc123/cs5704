from Framework.input_source import InputSource


class StubbedInputSource(InputSource):

    def __init__(self, revisions=None):
        rev1 = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "fd",
            "z"
        ]

        rev2 = [
            "a",
            "x",
            "c",
            "e",
            "y",
            "z.1"
        ]
        revisions = [rev1, rev2]
        self.revisions = revisions

    def get_files_with_revisions(self):
        return self.revisions
