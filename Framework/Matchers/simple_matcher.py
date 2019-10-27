
from fuzzywuzzy import fuzz

class SimpleMatcher():

    def evaluate_match(self, string_left:str, string_right):
        if string_left == string_right:
            return 'u'

        #partial match
        if fuzz.partial_ratio(string_left, string_right) > 90:
            return 'c'

        return 'unmatched'