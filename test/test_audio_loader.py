import pytest

from audio_import.audio_loader import sanitize_filename, UNIX_FORBIDDEN_CHAR, MS_FORBIDDEN_CHAR, ESCAPING_CHAR

def test_sanitize_filename():
    tested_and_expected_filenames = [
        ('there is nothing to remove from', 'there is nothing to remove from'),
        ("".join(UNIX_FORBIDDEN_CHAR), f"{ESCAPING_CHAR}" * len(UNIX_FORBIDDEN_CHAR)),
        ("".join(MS_FORBIDDEN_CHAR), f"{ESCAPING_CHAR}" * len(MS_FORBIDDEN_CHAR))
    ]
    for tested_and_expected_filename in tested_and_expected_filenames:
        tested_filename, expected_filename = tested_and_expected_filename
        assert sanitize_filename(tested_filename) == expected_filename
