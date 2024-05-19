import pytest

from audio_import import youtube_metadata_parser
from test.constants_for_test import FIRST_YOUTUBE_VIDEO_TITLE, FIRST_YOUTUBE_VIDEO_URL

def test_search_videos_on_youtube():
    assert len(youtube_metadata_parser.search_videos_on_youtube(FIRST_YOUTUBE_VIDEO_TITLE)) != 0

def test_get_exact_youtube_url_from_name():
    # Assume the test machine has an internet connection
    expected_url = FIRST_YOUTUBE_VIDEO_URL
    tested_url = youtube_metadata_parser.get_youtube_video_url(FIRST_YOUTUBE_VIDEO_TITLE)
    assert tested_url == expected_url
