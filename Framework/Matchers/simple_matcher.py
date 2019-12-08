
from fuzzywuzzy import fuzz


class SimpleMatcher:

    def evaluate_match(self, string_left:str, string_right):
        string_left = string_left.lstrip()
        string_right = string_right.lstrip()

        if string_left == string_right:
            return 'u'

        # print(string_left, fuzz.ratio(string_left, string_right), string_right, "\n")

        #partial match
        if fuzz.ratio(string_left, string_right) >= 70:
            return 'c'

        return 'unmatched'