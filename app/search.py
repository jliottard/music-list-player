from typing import List
from app.cannot_find_a_match_error import CannotFindAMatchError

def match_string_among_strings(searched_string: str, strings: List[str]) -> int:
    # Search a matching searched_name among strings, it ignores case
    # It does not necessary return the first match if there are multiples matches
    # Exception: raise a CannotFindAMatchError if there is no match, or the searched_string is empty
    if searched_string == "":
        if not "" in strings:
            raise CannotFindAMatchError
        else:
            return list(strings).index("")
    for string_index, string in enumerate(strings):
        if searched_string.lower() in string.lower():
            return string_index
    decomposed_string = searched_string.split(" ")
    for sub_string_component in decomposed_string:
        for sub_string_index, string in enumerate(strings):
            if sub_string_component.lower() in string.lower():
                return sub_string_index
    raise CannotFindAMatchError

def match_some_strings_among_strings(searched_arguments: List[str], expected_arguments: List[str]) -> int:
    # Search at least one matching string from searched_arguments among strings, ignore case
    # It does not necessary return the first match if there are multiples matches
    # @raise CannotFindAMatchError: if there is no match, or the only matching searched argument is an empty string to non-empty string
    for searched_argument in searched_arguments:
        for arg_index, expected_argument in enumerate(expected_arguments):
            if searched_argument == "" and expected_argument != "":
                continue
            if searched_argument.lower() in expected_argument.lower():
                return arg_index
    raise CannotFindAMatchError
