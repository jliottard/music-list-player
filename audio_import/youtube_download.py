import os

from pytubefix import exceptions, Stream, YouTube

from audio_import.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension
from app.file_management import remove_file_extension_part


def download_audio_from_youtube(youtube_url: str, output_directory_relative_path: str) -> str:
    """Download the video's audio to a MP3 file
    @param youtube_url: str a valid youtube video URL
    @param output_directory_relative_path; str filepath to save the download
    @returns str: an absolute path to the music audio
    @raises: CannotDownloadError if the download is not sucessful
    """
    try:
        youtube_stream: Stream = YouTube(youtube_url).streams.get_audio_only()
        audio_filepath: str = youtube_stream.download(mp3=True, output_path=output_directory_relative_path)
    except exceptions.VideoUnavailable as video_unavailable_error:
        raise CannotDownloadError(video_unavailable_error.args) from video_unavailable_error
    except exceptions.PytubeFixError as pytube_error:
        raise CannotDownloadError(pytube_error.args) from pytube_error
    
    # Rename downloaded file to file.mp3
    audio_mp3_filepath = remove_file_extension_part(audio_filepath) + FileExtension.MP3.value
    os.rename(audio_filepath, audio_mp3_filepath)
    return audio_mp3_filepath
