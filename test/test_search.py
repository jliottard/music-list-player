import pytest

from app import search
from app import cannot_find_a_match_error

def test_match_string_among_strings():
    assert search.match_string_among_strings("string", ["string"]) == 0
    assert search.match_string_among_strings("", [""]) == 0
    assert search.match_string_among_strings("", ["string", ""]) == 1
    assert search.match_string_among_strings("string", ["strings"]) == 0
    assert search.match_string_among_strings("string", ["STRING"]) == 0

def test_fails_match_string_among_strings():
    with pytest.raises(cannot_find_a_match_error.CannotFindAMatchError):
        search.match_string_among_strings("string", [""])
    with pytest.raises(cannot_find_a_match_error.CannotFindAMatchError):
        search.match_string_among_strings("", ["string"])

def test_match_some_strings_among_strings():
    assert search.match_some_strings_among_strings(["string", "int"], ["string", "float"]) == 0
    assert search.match_some_strings_among_strings(["string", "int"], ["list", "string"]) == 1
    assert search.match_some_strings_among_strings(["string", "int"], ["class", "float", "int"]) == 2
    assert search.match_some_strings_among_strings(["string", ""], ["class", "float", "int", ""]) == 3
    assert search.match_some_strings_among_strings(["string", "int"], ["STRING", "INT"]) in [0, 1]

def test_fails_match_some_strings_among_strings():
    with pytest.raises(cannot_find_a_match_error.CannotFindAMatchError):
        search.match_some_strings_among_strings(["string", "int"], ["", "float"])
    with pytest.raises(cannot_find_a_match_error.CannotFindAMatchError):
        search.match_some_strings_among_strings(["string", "int"], ["list", "float"])
    with pytest.raises(cannot_find_a_match_error.CannotFindAMatchError):
        search.match_some_strings_among_strings(["string", ""], ["class", "float", "int"])
