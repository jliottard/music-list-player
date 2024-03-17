import os
from typing import List

from app import configuration
from app.file_management import is_file_in_cache, _is_file_loaded
from app.interface import Interface
from audio.audio import Audio
from audio.file_extension import FileExtension
from audio.playlist import Playlist
from audio_import import youtube_download, youtube_metadata_parser
from audio_import.cannot_download_error import CannotDownloadError
from audio_import.plain_text_parse import parse_plain_text_playlist_file
from audio_import.youtube_video_metadata import YouTubeVideoMetadata

def _choose_youtube_video_interactively(video_metadatas: List[YouTubeVideoMetadata], user_interface: Interface) -> YouTubeVideoMetadata|None:
    """Ask the terminal's user by a command line interaction to select a YouTube video from the list
    @param video_metadatas: List[YouTubeVideoMetadata] the list of YouTube videos to choose from
    @param user_interface: Interface user's interface, assume the user's input is booked
    @return: YouTubeVideoMetadata|None the choosen one, or nothing if no metadata were chosen
    """
    has_user_confirmed_result = False
    chosen_video_metadata: YouTubeVideoMetadata = None
    for youtube_metadata in video_metadatas:
        prompted_request = "Request: Would you like to download the following YouTube video's audio ?"
        prompted_request += " (type 'yes' to confirm or type any to show next result):"
        user_interface.request_output_to_user(prompted_request)
        prompted_video_proposition = " ".join(
            [
                f"- Title: \"{youtube_metadata.title}\"",
                f"by \"{youtube_metadata.author}\"",
                f"(duration: {youtube_metadata.duration})"
            ]
        )
        user_interface.request_output_to_user(prompted_video_proposition)
        user_input: str = user_interface.receive_input_from_user()
        has_user_confirmed_result = user_input == 'yes'
        if has_user_confirmed_result:
            chosen_video_metadata = youtube_metadata
            break
    return chosen_video_metadata

def load(audio_name: str, file_extension: FileExtension, profile: str, user_interface: Interface) -> Audio:
    """Load the audio from the cache or from the Internet
    @param audio_name: str
    @param file_extension: FileExtension
    @param user_interface: Interface, assume the user's input is booked
    @return: an Audio or None if the audio could not be found or downloaded
    """
    returned_audio = None
    if _is_file_loaded(audio_name + file_extension.value, profile):
        user_interface.request_output_to_user(f"Info: the audio \"{audio_name}\" is found in cache memory.")
        returned_audio = Audio(
            name=audio_name,
            filepath=configuration.get_audio_file_path(audio_name + file_extension.value, profile),
            file_extension=file_extension
        )
    else:
        user_interface.request_output_to_user(
            f"Info: the audio \"{audio_name}\" is not found in cache memory. Downloading audio from internet."
        )

        youtube_videos_metadatas: List[YouTubeVideoMetadata] = youtube_metadata_parser.search_videos_on_youtube(audio_name)
        chosen_youtube_video: YouTubeVideoMetadata = _choose_youtube_video_interactively(
            video_metadatas=youtube_videos_metadatas,
            user_interface=user_interface
        )
        youtube_video_url: str = chosen_youtube_video.url
        try:
            audio_download_absolute_path = youtube_download.download_audio_from_youtube(
                youtube_url=youtube_video_url,
                output_directory_relative_path=configuration.get_audios_directory_path(profile)
            )
        except CannotDownloadError as video_cannot_be_downloaded:
            user_interface.request_output_to_user(
                f"Warning: the video {audio_name} could not be downloaded because {video_cannot_be_downloaded}"
            )
            return None
        # Rename the file having Youtube video title as name to the audio name
        #  from the playlist file
        _drive, path_and_file = os.path.splitdrive(audio_download_absolute_path)
        path, _file = os.path.split(path_and_file)
        playlist_name_like_audio_absolute_path = os.path.join(path, audio_name + file_extension.value)
        os.rename(audio_download_absolute_path, playlist_name_like_audio_absolute_path)
        returned_audio = Audio(
            name=audio_name,
            filepath=configuration.operating_system_proof_path(playlist_name_like_audio_absolute_path),
            file_extension=file_extension
        )
    return returned_audio

def iterate_over_loading_playlist(playlist_file_absolute_path: str, playlist_profile: str, user_interface: Interface) -> List[Audio]:
    """Parse playlist file and load the music into cache
    @param playlist_file_absolute_path a filepath of the text file describing the music playlist
    @param playlist_profile: str
    @param user_interface: Interface, assume the user's input is booked
    @yield: Audio
    """
    playlist_lines: list[str] = parse_plain_text_playlist_file(playlist_file_absolute_path, user_interface)
    for audio_name in playlist_lines:
        maybe_audio: Audio = load(audio_name, FileExtension.MP3, playlist_profile, user_interface)
        if maybe_audio is None:
            continue
        yield maybe_audio

def unload_music(audio: Audio, profile: str) -> None:
    """Remove the local audio is found"""
    if _is_file_loaded(audio.name + audio.extension.value, profile):
        cached_audio_filepath: str = configuration.get_audio_file_path(audio.name + audio.extension.value, profile)
        os.remove(cached_audio_filepath)
    if audio.lyrics_filepath is not None and is_file_in_cache(audio.lyrics_filepath):
        os.remove(configuration.get_audio_file_path(audio.lyrics_filepath, profile))


def flush_playlist_cache(playlist: Playlist, playlist_profile: str) -> None:
    """Description: Remove playlist cached files
    @param playlist: Playlist: the playlist containing the audio to remove from cache
    """
    for playlist_audio in playlist.audios:
        unload_music(playlist_audio, playlist_profile)
