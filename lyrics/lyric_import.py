import syncedlyrics

from app.config.configuration import Configuration, TEXT_ENCODING
from app.interface import Interface
from app.file_management import is_file_in_cache
from audio.audio import Audio

COEF_SEC_TO_MS = 10 ** 3

def prepare_lyrics(audio: Audio, configuration: Configuration, user_interface: Interface) -> None:
    """Load the lyrics locally or download it remotely if the audio's lyric can be found
    If the lyrics cannot be found the lyrics_filepath field of the audio is None
    @param audio: Audio: the audio to search lyrics for
    @param configuration: Configuration: the in-used configuration
    @param user_interface: Interface
    @raise TypeError: if the local lyric file is not in a LRC format
    """
    lyric_filename = f"{audio.name}.lrc"
    lyric_filepath = configuration.get_audio_file_path(lyric_filename)
    if is_file_in_cache(lyric_filepath):
        audio.lyrics_filepath = lyric_filepath
    else:
        audio.lyrics_filepath = None
        if configuration.is_music_lyrics_searched_on_import():
            try:
                user_interface.request_output_to_user(
                    f"Info: searching the lyrics of \"{audio.name}\" on Internet."
                )
                maybe_lyric_text = syncedlyrics.search(audio.name, save_path=lyric_filepath)
                if maybe_lyric_text is not None:
                    with open(lyric_filepath, 'wt', encoding=TEXT_ENCODING) as lyric_file:
                        lyric_file.write(maybe_lyric_text)
                    audio.lyrics_filepath = lyric_filepath
                    return True
                else:
                    audio.lyrics_filepath = None
            except TypeError:
                audio.lyrics_filepath = None
