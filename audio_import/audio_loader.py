import os
from typing import List

from app.cannot_find_a_match_error import CannotFindAMatchError
from app.config.configuration import Configuration, operating_system_proof_path
from app.file_management import is_file_in_cache, _is_file_loaded
from app.interface import Interface
from app.search import match_some_strings_among_strings
from audio.audio import Audio
from audio.file_extension import FileExtension
from audio.playlist import Playlist
from audio_import import youtube_download, youtube_metadata_parser
from audio_import.audio_metadata import AudioMetadata
from audio_import.cannot_download_error import CannotDownloadError
from audio_import.youtube_video_metadata import YouTubeVideoMetadata

UNIX_FORBIDDEN_CHAR = ['/', '\0']
MS_FORBIDDEN_CHAR = ['/', '\\', '*', ':', '?', '"', '<', '>', '|', '\0']
ESCAPING_CHAR = '_'
IO_ERROR_NO_SPACE_LEFT_NUMBER = 28

def _choose_youtube_video_interactively(video_metadatas: List[YouTubeVideoMetadata], user_interface: Interface) -> YouTubeVideoMetadata|None:
    """Ask the terminal's user by a command line interaction to select a YouTube video from the list
    @param video_metadatas: List[YouTubeVideoMetadata] the list of YouTube videos to choose from
    @param user_interface: Interface user's interface, assume the user's input is booked
    @return: YouTubeVideoMetadata | None the choosen audio to download, or None if no metadata were chosen correctly
    """
    number_of_choices = len(video_metadatas)
    user_interface.request_output_to_user(" ".join(
            [
                "Request: Which audio you like to download from the following YouTube videos ?",
                "(type the number of one of the following proposed audios from YouTube):"
            ]
        )
    )
    starting_index = 1
    for choice_position, youtube_metadata in enumerate(video_metadatas):
        user_interface.request_output_to_user(" ".join(
                [
                    f"({choice_position + starting_index}/{number_of_choices})",
                    f"- Title: \"{youtube_metadata.title}\"",
                    f"by \"{youtube_metadata.author}\"",
                    f"(duration: {youtube_metadata.duration})"
                ]
            )
        )
    user_input: str = user_interface.receive_input_from_user()
    try:
        while not starting_index <= int(user_input) <= number_of_choices:
            user_interface.request_output_to_user(
                " ".join(
                    [
                        f"Warning: the requested audio's number (\"{user_input}\") is invalid.",
                        f"Please choose a number from {starting_index} to {number_of_choices}"
                    ]
                )
            )
            user_input: str = user_interface.receive_input_from_user()
        return video_metadatas[int(user_input) - starting_index]
    except ValueError as value_error:
        user_interface.request_output_to_user(" ".join(
                [
                    f"Warning: the requested audio's number's format (\"{user_input}\") is invalid."
                    f"More details: {value_error.args}"
                ]
            )
        )
        return None

def _get_first_youtube_result(video_metadatas: List[YouTubeVideoMetadata]) -> YouTubeVideoMetadata|None:
    """Return the YouTube result
    @param video_metadatas: List[YouTubeVideoMetadata]
    @return: YouTubeVideoMetadata|None the choosen one, or nothing if no metadata were chosen
    """
    return video_metadatas[0] if len(video_metadatas) != 0 else None

def _rename_filename(source_filepath: str, new_filename: str) -> str:
    """Rename just the filename of the given file
    @param source_filepath: str: the path of the file to rename
    @param new_filename: str: the filename rename
    @return str: the new filepath as an absolute filepath
    """
    _drive, path_and_file = os.path.splitdrive(source_filepath)
    path, _file = os.path.split(path_and_file)
    playlist_name_like_audio_absolute_path = os.path.join(path, new_filename)
    os.rename(source_filepath, playlist_name_like_audio_absolute_path)
    return operating_system_proof_path(playlist_name_like_audio_absolute_path)

def load(audio_name: str, file_extension: FileExtension, configuration: Configuration,
         user_interface: Interface, only_local: bool, maybe_source: str | None) -> Audio:
    """Load the audio from the cache or from the Internet
    @param audio_name: str
    @param file_extension: FileExtension
    @param configuration: COnfiguration
    @param user_interface: Interface, assume the user's input is booked
    @param only_local: bool only try to load local audios
    @param maybe_source: str | None: the YouTube URL to the audio source
    @return: an Audio or None if the audio could not be found or downloaded
    @raise IOError
    """
    returned_audio = None
    if _is_file_loaded(audio_name + file_extension.value, configuration):
        user_interface.request_output_to_user(f"Info: the audio \"{audio_name}\" is found in cache memory.")
        returned_audio = Audio(
            name=audio_name,
            filepath=configuration.get_audio_file_path(audio_name + file_extension.value),
            file_extension=file_extension
        )
    elif not only_local:
        user_interface.request_output_to_user(
            f"Info: the audio \"{audio_name}\" is not found in cache memory. Trying to download it from Internet."
        )
        youtube_videos_metadatas: List[YouTubeVideoMetadata] = youtube_metadata_parser.search_videos_on_youtube(audio_name)
        if configuration.is_audio_source_selected_on_import():
            maybe_chosen_youtube_video: YouTubeVideoMetadata | None = _choose_youtube_video_interactively(
                video_metadatas=youtube_videos_metadatas,
                user_interface=user_interface
            )
        else:
            if maybe_source is not None:
                maybe_chosen_youtube_video = _get_first_youtube_result(youtube_metadata_parser.search_videos_on_youtube(maybe_source))
            else:
                maybe_chosen_youtube_video: YouTubeVideoMetadata | None = _get_first_youtube_result(youtube_videos_metadatas)
        if maybe_chosen_youtube_video is None:
            user_interface.request_output_to_user(
                "Warning: no audio could not be downloaded because no proposed audio was selected."
            )
            return None
        chosen_youtube_video: YouTubeVideoMetadata = maybe_chosen_youtube_video
        try:
            audio_download_absolute_path = youtube_download.download_audio_from_youtube(
                youtube_url=chosen_youtube_video.url,
                output_directory_relative_path=configuration.get_audios_directory_path()
            )
        except CannotDownloadError as video_cannot_be_downloaded:
            user_interface.request_output_to_user(
                f"Warning: the audio \"{audio_name}\" could not be downloaded because {video_cannot_be_downloaded}"
            )
            return None
        except IOError as io_error:
            user_interface.request_output_to_user(
                f"Warning: the audio \"{audio_name}\" cannot be downloaded because {io_error.strerror}"
            )
            raise io_error
        # Rename the file having Youtube video title as name to the audio name
        #  from the playlist file
        renamed_filepath = _rename_filename(
            source_filepath=audio_download_absolute_path,
            new_filename=audio_name + file_extension.value
        )
        returned_audio = Audio(
            name=audio_name,
            filepath=renamed_filepath,
            file_extension=file_extension
        )
    return returned_audio

def sanitize_filename(filename: str) -> str:
    """ Escape characters from the given filename that would be interpreted in a filepath context
        @param filename: str
        @return str: the filename sanitized
    """
    sanitized_name = list(filename)
    for i, char in enumerate(sanitized_name):
        if char in UNIX_FORBIDDEN_CHAR or char in MS_FORBIDDEN_CHAR:
            sanitized_name[i] = ESCAPING_CHAR
    return ''.join(sanitized_name)

def iterate_over_loading_playlist(configuration: Configuration, meta_query: AudioMetadata, user_interface: Interface) -> List[Audio]:
    """Parse playlist file and load the music into cache
    @param configuration: Configuration
    @param meta_query: AudioMetada
    @param user_interface: Interface, assume the user's input is booked
    @yield: Audio
    """
    load_only_local_audio = False
    for audio_metadata in configuration.profile.audio_metadatas:
        name = sanitize_filename(audio_metadata.name)
        any_tags = audio_metadata.tags
        if len(meta_query.tags) != 0:
            try:
                match_some_strings_among_strings(any_tags, meta_query.tags)
            except CannotFindAMatchError:
                # the current audio's metadata does not match the query's tags
                continue
        maybe_audio = None
        try:
            maybe_audio: Audio = load(
                audio_name=name,
                file_extension=FileExtension.MP3,
                configuration=configuration,
                user_interface=user_interface,
                only_local=load_only_local_audio,
                maybe_source=audio_metadata.source
            )
        except IOError as io_error:
            if io_error.errno == IO_ERROR_NO_SPACE_LEFT_NUMBER:
                user_interface.request_output_to_user(
                    'Warning: Since there is no more memory space left for downloading, only local audios will be loaded from now.'
                )
                load_only_local_audio = True
            else:
                user_interface.request_output_to_user(
                    f"Warning: IOError returned {str(io_error)}"
                )
        if maybe_audio is None:
            continue
        audio: Audio = maybe_audio
        yield audio

def unload_music(audio: Audio, configuration: Configuration) -> None:
    """Remove the local audio is found"""
    if _is_file_loaded(audio.name + audio.extension.value, configuration):
        cached_audio_filepath: str = configuration.get_audio_file_path(audio.name + audio.extension.value)
        os.remove(cached_audio_filepath)
    if audio.lyrics_filepath is not None and is_file_in_cache(audio.lyrics_filepath):
        os.remove(configuration.get_audio_file_path(audio.lyrics_filepath))

def flush_playlist_cache(playlist: Playlist, configuration: Configuration) -> None:
    """Description: Remove playlist cached files
    @param playlist: Playlist: the playlist containing the audio to remove from cache
    @param configuration: Configuration
    """
    for playlist_audio in playlist.audios:
        unload_music(playlist_audio, configuration)
