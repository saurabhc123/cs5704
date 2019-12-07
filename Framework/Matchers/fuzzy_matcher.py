
from fuzzywuzzy import fuzz


class FuzzyMatcher:

    def evaluate_match(self, string_left: str, string_right: str):
        if string_left == string_right:
            return 'u'

        else:
            return fuzz.partial_ratio(string_left, string_right)