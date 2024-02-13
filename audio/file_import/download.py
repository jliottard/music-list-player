import os, sys
import requests
from pytube import YouTube
from pytube import exceptions

from audio.file_import.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension

def get_youtube_video_url(music_name: str) -> str:
    # Input: - music_name: string of the format "NAME AUTHOR" of the music video to search
    # Output: youtube URL of the first result of the searched music
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

def download_audio_from_youtube(youtube_url: str, output_directory_relative_path: str) -> str:
    # Description: Download the video's audio to a MP3 file
    # Input: a valid youtube video URL
    # Output: an absolute path to the music audio
    # Exceptions: can throw a CannotDownloadError if the download is not
    # sucessful
    try:
        audio_filepath = YouTube(youtube_url).streams.filter(only_audio=True).first().download(
            output_path=output_directory_relative_path
        )
    except exceptions.AgeRestrictedError as video_is_age_restricted_error:
        raise CannotDownloadError(video_is_age_restricted_error.args)
    except exceptions.LiveStreamError as video_is_live_stream_error:
        raise CannotDownloadError(video_is_live_stream_error.args)
    except exceptions.VideoRegionBlocked as video_is_region_blocked:
        raise CannotDownloadError(video_is_region_blocked.args)
    except Exception as other_exception:
        raise CannotDownloadError(other_exception.args)
    # Rename downloaded file to file.mp3
    name_base, _video_extension = os.path.splitext(audio_filepath)
    audio_mp3_filepath = name_base + FileExtension.MP3.value
    os.rename(audio_filepath, audio_mp3_filepath)
    return audio_mp3_filepath
