import os

from app import configuration
from audio.audio import Audio
from audio.file_import import download
from audio.file_import.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension

def _parse_playlist_text_file(playlist_file_absolute_path: str) -> list[str]:
    """ Return the music name in a list """
    print("Parsing playlist file.")
    with open(playlist_file_absolute_path, "rt", encoding=configuration.TEXT_ENCODING) as playlist_file:
        lines = playlist_file.readlines()
        def remove_carriage_return(string):
            return string.strip("\n")
        return list(map(remove_carriage_return, lines))

def _is_audio_in_cache(absolute_audio_path: str) -> bool:
    return os.path.exists(absolute_audio_path)

def _is_audio_loaded(audio_name: str, file_extension: FileExtension, profile: str) -> bool:
    audio_file_path: str = configuration.get_audio_file_path(audio_name + file_extension.value, profile)
    return _is_audio_in_cache(audio_file_path)

def load(audio_name: str, file_extension: FileExtension, profile: str) -> Audio:
    """
    Load the audio from the cache or from the Internet
    @return: an Audio or None if the audio could not be found or downloaded
    """
    if _is_audio_loaded(audio_name, file_extension, profile):
        print(f"The audio \"{audio_name}\" is found in cache.")
        return Audio(
            name=audio_name,
            filepath=configuration.get_audio_file_path(audio_name + file_extension.value, profile),
            file_extension=file_extension
        )
    print(f"The audio \"{audio_name}\" is not found in cache. Downloading audio from internet.")
    youtube_video_url: str = download.get_youtube_video_url(audio_name)
    try:
        audio_download_absolute_path = download.download_audio_from_youtube(
            youtube_url=youtube_video_url,
            output_directory_relative_path=configuration.get_audios_directory_path(profile)
        )
    except CannotDownloadError as video_cannot_be_downloaded:
        print(f"Warning: the video {audio_name} could not be downloaded due to {video_cannot_be_downloaded}")
        return None
    # Rename the file having Youtube video title as name to the audio name
    #  from the playlist file
    _drive, path_and_file = os.path.splitdrive(audio_download_absolute_path)
    path, _file = os.path.split(path_and_file)
    playlist_name_like_audio_absolute_path = os.path.join(path, audio_name + file_extension.value)
    os.rename(audio_download_absolute_path, playlist_name_like_audio_absolute_path)
    return Audio(
        name=audio_name,
        filepath=configuration.operating_system_proof_path(playlist_name_like_audio_absolute_path),
        file_extension=file_extension
    )

def import_playlist_audios(playlist_file_absolute_path: str, playlist_profile: str) -> list[Audio]:
    """
    Description: Parse playlist file
    @param playlist_file_absolute_path a filepath of the text file describing the music playlist
    @return a list of the audios
    """
    playlist_lines: list[str] = _parse_playlist_text_file(playlist_file_absolute_path)
    audios: list[Audio] = []
    for audio_name in playlist_lines:
        maybe_audio: Audio = load(audio_name, FileExtension.MP3, playlist_profile)
        if maybe_audio is None:
            continue
        audios.append(maybe_audio)
    return audios
