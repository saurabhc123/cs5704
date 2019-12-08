
from fuzzywuzzy import fuzz


class SimpleMatcher:

    def evaluate_match(self, string_left: str, string_right: str):
        string_left = string_left.lstrip()
        string_right = string_right.lstrip()

        # print(string_left)
        # print(string_right)

        if string_left == string_right:
            return 'u'

        # print(string_left, fuzz.ratio(string_left, string_right), string_right)
        # print()

        #partial match
        if fuzz.ratio(string_left, string_right) >= 70:
            # print(string_left + " ", str(fuzz.partial_ratio(string_left, string_right), " " + string_right))
            return 'c'

        return 'unmatched'