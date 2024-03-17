import os, sys
import requests
from pytube import YouTube
from pytube import exceptions

from audio_import.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension


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
