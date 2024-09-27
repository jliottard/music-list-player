from os import path
import os
import pytest

from app.config.configuration import operating_system_proof_path
from audio_import import cannot_download_error, youtube_download, youtube_metadata_parser
from test.conftest import TEST_WORK_DIRECTORY_RELATIVE_PATH
from test.constants_for_test import FIRST_YOUTUBE_VIDEO_TITLE, FIRST_YOUTUBE_VIDEO_URL, LONGEST_YOUTUBE_LIVE_TITLE

def test_download_audio_from_youtube_from_valid_url():
    # Assume the test machine has an internet connection
    tested_url = FIRST_YOUTUBE_VIDEO_URL
    expected_download_audio_from_youtube_filepath = operating_system_proof_path(path.abspath(path.join(
        TEST_WORK_DIRECTORY_RELATIVE_PATH,
        FIRST_YOUTUBE_VIDEO_TITLE + ".mp3"
    )))
    tested_audio_filepath = youtube_download.download_audio_from_youtube(tested_url, TEST_WORK_DIRECTORY_RELATIVE_PATH)
    assert tested_audio_filepath == expected_download_audio_from_youtube_filepath
    assert path.isfile(expected_download_audio_from_youtube_filepath)
    assert path.getsize(expected_download_audio_from_youtube_filepath) > 1

def test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_with_wrong_url():
    # Assume the test machine has an internet connection
    with pytest.raises(cannot_download_error.CannotDownloadError):
        youtube_download.download_audio_from_youtube("https://youtube.com/invalid_url", TEST_WORK_DIRECTORY_RELATIVE_PATH)

def test_fails_download_audio_from_youtube_raise_cannot_download_error_exception_is_a_livestream():
    # Assume the test machine has an internet connection
    lofi_girl_livestream_url = youtube_metadata_parser.get_youtube_video_url(LONGEST_YOUTUBE_LIVE_TITLE)
    with pytest.raises(cannot_download_error.CannotDownloadError):
        youtube_download.download_audio_from_youtube(lofi_girl_livestream_url, TEST_WORK_DIRECTORY_RELATIVE_PATH)
