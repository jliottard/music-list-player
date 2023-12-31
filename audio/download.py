import os, sys
import requests
from pytube import YouTube

def get_youtube_video_url(music_name: str) -> str:
    # Input: - music_name: string of the format "NAME AUTHOR" of the music video to search
    # Output: youtube URL of the first result of the searched music
    music_name = music_name.strip()
    music_name_url = music_name.replace(' ', '+')
    youtube_research_url = 'https://www.youtube.com/results?search_query='
    html_response = requests.get(youtube_research_url + music_name_url)
    html_contents = html_response.text
    video_id_start_keyword = '/watch?v='
    start_index = html_contents.find(video_id_start_keyword)
    video_id_end_keyword = '\\u'
    end_index = html_contents.find(video_id_end_keyword, start_index)
    watch_video_url_part = html_contents[start_index:end_index]
    music_video_url = 'https://www.youtube.com/' + watch_video_url_part
    return music_video_url

def download_audio(youtube_url: str, output_directory_relative_path: str) -> str:
    # Description: Download the video's audio to a MP3 file
    # Input: a valid youtube video URL
    # Output: an absolute path to the music audio
    audio_filepath = YouTube(youtube_url).streams.filter(only_audio=True).first().download(output_path=output_directory_relative_path)
    # Rename downloaded file to file.mp3
    name_base, _video_extension = os.path.splitext(audio_filepath)
    audio_mp3_filepath = name_base + '.mp3'
    os.rename(audio_filepath, audio_mp3_filepath)
    return audio_mp3_filepath
