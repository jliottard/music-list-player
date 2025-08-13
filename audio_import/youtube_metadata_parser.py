from typing import List
import requests
# from youtubesearchpython import VideosSearch
from pytubefix import Search

from audio_import.youtube_video_metadata import YouTubeVideoMetadata

def search_videos_on_youtube(term_search: str) -> List[YouTubeVideoMetadata]:
    """ Search on YouTube for videos
        @param term_search: str the YouTube search
        @return List[YouTubeVideoMetadata] a list of the video metadata got by the search
    """
    results = Search(term_search)
    VIDEO_LIMIT = 5
    metadatas: list = []
    video_result_count = 0
    for video in results.videos:
        metadata = YouTubeVideoMetadata(
            video_id=video.video_id,
            url=video.watch_url,
            title=video._title,
            author=video._author,
            duration=None,
            views=None,
            publication_date=video._publish_date
        )
        metadatas.append(metadata)
        video_result_count += 1
        if video_result_count >= VIDEO_LIMIT:
            break
    return metadatas

def get_youtube_video_url(music_name: str) -> str:
    """Search the YouTube URL for the given music_name as a search term
        @param music_name: str string of the format "NAME AUTHOR" of the music video to search
        @return: str youtube URL of the first result of the searched music
    """
    music_name = music_name.strip()
    music_name_url = music_name.replace(' ', '+')
    youtube_research_url = 'https://www.youtube.com/results?search_query='
    html_response = requests.get(youtube_research_url + music_name_url, timeout=20)
    html_contents = html_response.text
    video_id_start_keyword = '/watch?v='
    start_index = html_contents.find(video_id_start_keyword)
    video_id_end_keyword = '\\u'
    end_index = html_contents.find(video_id_end_keyword, start_index)
    watch_video_url_part = html_contents[start_index:end_index]
    music_video_url = 'https://www.youtube.com' + watch_video_url_part
    return music_video_url

def is_url_refering_to_youtube(url: str) -> bool:
    return "youtu.be" in url or "youtube.com" in url
