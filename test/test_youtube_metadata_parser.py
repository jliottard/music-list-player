from audio_import.youtube_metadata_parser import search_videos_on_youtube, get_youtube_video_url

from test.constants_for_test import FIRST_YOUTUBE_VIDEO_TITLE, FIRST_YOUTUBE_VIDEO_URL

def test_search_videos_on_youtube():
    assert len(search_videos_on_youtube(FIRST_YOUTUBE_VIDEO_TITLE)) != 0

def test_search_videos_on_youtube_first_youtube_video():
    youtube_metadatas = search_videos_on_youtube(FIRST_YOUTUBE_VIDEO_TITLE)
    assert youtube_metadatas[0].url == FIRST_YOUTUBE_VIDEO_URL

def test_get_exact_youtube_url_from_name():
    # Assume the test machine has an internet connection
    expected_url = FIRST_YOUTUBE_VIDEO_URL
    tested_url = get_youtube_video_url(FIRST_YOUTUBE_VIDEO_TITLE)
    assert tested_url == expected_url
