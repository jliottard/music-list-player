from typing import List
import requests
from youtubesearchpython import VideosSearch

from audio_import.youtube_video_metadata import YouTubeVideoMetadata

def search_videos_on_youtube(term_search: str) -> List[YouTubeVideoMetadata]:
    """ Search on YouTube for videos
        @param term_search: str the YouTube search
        @return List[YouTubeVideoMetadata] a list of the video metadata got by the search
    """
    videos_search = VideosSearch(term_search, limit=5)
    results: dict = videos_search.result()['result']
    metadatas: list = []
    for result in results:
        metadatas.append(
            YouTubeVideoMetadata(
                video_id=result['id'],
                link=result['link'],
                title=result['title'],
                author=result['channel']['name'],
                duration=result['duration'],
                views=result['viewCount']['text'],
                publish_date=result['publishedTime']
            )
        )
    return metadatas

def get_youtube_video_url(music_name: str) -> str:
    """
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