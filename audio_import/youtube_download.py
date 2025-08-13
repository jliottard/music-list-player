import os

from pytubefix import exceptions, Stream, YouTube

from audio_import.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension
from app.file_management import remove_file_extension_part


def download_audio_from_youtube(youtube_url: str, output_directory_relative_path: str, file_extension: FileExtension) -> str:
    """Download the video's audio to a file
    @param youtube_url: str a valid youtube video URL
    @param output_directory_relative_path: str filepath to save the download
    @param file_extension: FileExtension the file extension of the downloaded audio file
    @returns str: an absolute path to the music audio
    @raises: CannotDownloadError if the download is not successful
    """
    try:
        maybe_youtube_stream: Stream | None = YouTube(youtube_url).streams.get_audio_only()
        match maybe_youtube_stream:
            case None:
                raise CannotDownloadError("Youtube audio stream source not found")
            case _:
                audio_filepath: str = maybe_youtube_stream.download(output_path=output_directory_relative_path)
    except exceptions.VideoUnavailable as video_unavailable_error:
        raise CannotDownloadError(video_unavailable_error.args) from video_unavailable_error
    except exceptions.PytubeFixError as pytube_error:
        raise CannotDownloadError(pytube_error.args) from pytube_error
    
    # Rename downloaded file to file.<file_extension>
    audio_with_ext_filepath = remove_file_extension_part(audio_filepath) + file_extension.value
    os.rename(audio_filepath, audio_with_ext_filepath)
    return audio_with_ext_filepath
