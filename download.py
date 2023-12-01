import os, sys
import requests
from pytube import YouTube

def get_youtube_url(music_name_author_line: str) -> str:
    # Input: raw_music_line: string of the format "NAME - AUTHOR" of the music video
    # to search
    # Output: youtube URL of the searched music
    name, author = music_name_author_line.split("-")
    name = name.strip()
    author = author.strip()
    youtube_research_url = "https://www.youtube.com/results?search_query="
    name_author_url = name.replace(" ", "+") + "+" + author.replace(" ", "+")
    html_response = requests.get(youtube_research_url + name_author_url)
    html_contents = html_response.text
    video_id_start_keyword = "/watch?v="
    start_index = html_contents.find(video_id_start_keyword)
    video_id_end_keyword = "\\u"
    end_index = html_contents.find(video_id_end_keyword, start_index)
    watch_video_url_part = html_contents[start_index:end_index]
    music_video_url = "https://www.youtube.com/" + watch_video_url_part
    return music_video_url

def download_audio(youtube_url: str) -> str:
    # Input: a valid youtube video URL
    # Output: an absolute path to the music audio
    audio_filepath = YouTube(youtube_url).streams.filter(only_audio=True).first().download(output_path="audios")
    name_base, video_extension = os.path.splitext(audio_filepath)
    audio_extension_filepath = name_base + '.mp3'
    os.rename(audio_filepath, audio_extension_filepath)
    print(f"Audio file saved at {audio_extension_filepath}")
    return audio_extension_filepath

