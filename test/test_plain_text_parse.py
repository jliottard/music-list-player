import pytest

from audio_import.plain_text_parse import remove_metadata, try_extract_web_url, try_extract_tags

from test.constants_for_test import FIRST_YOUTUBE_VIDEO_URL

def test_try_extract_web_url():
    tested_and_expected_urls = [
        (FIRST_YOUTUBE_VIDEO_URL, FIRST_YOUTUBE_VIDEO_URL),
        ('there is no URL here', None),
        (f"[{FIRST_YOUTUBE_VIDEO_URL}]", FIRST_YOUTUBE_VIDEO_URL),
        (f"({FIRST_YOUTUBE_VIDEO_URL})", FIRST_YOUTUBE_VIDEO_URL),
        (f"{FIRST_YOUTUBE_VIDEO_URL} {FIRST_YOUTUBE_VIDEO_URL}", FIRST_YOUTUBE_VIDEO_URL)
    ]

    for tested_and_expected_url in tested_and_expected_urls:
        tested_url, expected_url = tested_and_expected_url
        assert try_extract_web_url(tested_url) == expected_url

def test_try_extract_tags():
    tested_and_expected_tags = [
        ('there is no tag here either', []),
        ('#tag', ['#tag']),
        ('#first #second', ['#first', '#second']),
        ('#connected_tags#are_accepted', ['#connected_tags', '#are_accepted']),
        ('#tag#alone# is ignored', ['#tag', '#alone']),
        ('#dash-is-accepted-within-a-tag', ['#dash-is-accepted-within-a-tag']),
        ('#underscore_is_accepted_within_a_tag', ['#underscore_is_accepted_within_a_tag']),
        ('#no_space is #allowed_within_a_tag', ['#no_space', '#allowed_within_a_tag'])
    ]
    for tested_and_expected_tag in tested_and_expected_tags:
        tested_tag_string, expected_tags = tested_and_expected_tag
        assert try_extract_tags(tested_tag_string) == expected_tags

def test_remove_metadata():
    tested_and_expected_metadatas = [
        ('there is no metadata in this line for sure', 'there is no metadata in this line for sure'),
        ('there is a #tag here', 'there is a here'),
        ('there are #multiple tags #for-sure', 'there are tags'),
        (f"there is an URL {FIRST_YOUTUBE_VIDEO_URL} right before", 'there is an URL right before')
    ]
    for tested_and_expected_metadata in tested_and_expected_metadatas:
        tested_metadata_line, expected_line = tested_and_expected_metadata
        assert remove_metadata(tested_metadata_line) == expected_line
