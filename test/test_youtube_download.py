from os import path
import os
import pytest

from audio_import import cannot_download_error, youtube_download, youtube_metadata_parser
from test.constants_for_test import FIRST_YOUTUBE_VIDEO_TITLE, FIRST_YOUTUBE_VIDEO_URL, LONGEST_YOUTUBE_LIVE_TITLE

@pytest.fixture
def test_teardown_of_test_download_audio_from_youtube_from_valid_url():
    yield
    os.remove(path.abspath(path.join("test", FIRST_YOUTUBE_VIDEO_TITLE + ".mp3")))

def test_download_audio_from_youtube_from_valid_url(test_teardown_of_test_download_audio_from_youtube_from_valid_url):
    # Assume the test machine has an internet connection
    testing_url = FIRST_YOUTUBE_VIDEO_URL
    testing_directory = "test"
    expected_download_audio_from_youtube_filepath = path.abspath(path.join("test", FIRST_YOUTUBE_VIDEO_TITLE + ".mp3"))
    tested_audio_filepath = youtube_download.download_audio_from_youtube(testing_url, testing_directory)
    assert tested_audio_filepath == expected_download_audio_from_youtube_filepath
    assert path.isfile(expected_download_audio_from_youtube_filepath)
    assert path.getsize(expected_download_audio_from_youtube_filepath) > 1

def test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_with_wrong_url():
    # Assume the test machine has an internet connection
    with pytest.raises(cannot_download_error.CannotDownloadError):
        youtube_download.download_audio_from_youtube("https://youtube.com/invalid_url", "test")

@pytest.fixture
def test_teardown_of_test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_is_a_livestream():
    yield
    unexpected_file_filepath = path.abspath(path.join("test", LONGEST_YOUTUBE_LIVE_TITLE + ".mp3"))
    if path.isfile(unexpected_file_filepath):
        os.remove(unexpected_file_filepath)

def test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_is_a_livestream(test_teardown_of_test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_is_a_livestream):
    # Assume the test machine has an internet connection
    lofi_girl_livestream_url = youtube_metadata_parser.get_youtube_video_url(LONGEST_YOUTUBE_LIVE_TITLE)
    with pytest.raises(cannot_download_error.CannotDownloadError):
        youtube_download.download_audio_from_youtube(lofi_girl_livestream_url, "test")
