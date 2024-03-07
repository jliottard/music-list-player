import syncedlyrics

from app import configuration
from app.file_management import _is_file_in_cache
from audio.audio import Audio

COEF_SEC_TO_MS = 10 ** 3

def prepare_lyrics(audio: Audio, profile: str) -> bool:
    ''' Load the lyrics if the audio's lyric can be found
    @param audio: Audio: the audio to search lyrics for
    @param profile: str: the in-use configuration profile
    @return bool: True if the lyrics have been loaded or False 
    '''
    lyric_filename = f"{audio.name}.lrc"
    lyric_filepath = configuration.get_audio_file_path(lyric_filename, profile)
    if _is_file_in_cache(lyric_filepath):
        audio.lyrics_filepath = lyric_filepath
    else:
        audio.lyrics_filepath = None
        if configuration.is_music_lyrics_searched_on_import(profile):
            try:
                maybe_lyric_text = syncedlyrics.search(audio.name, save_path=lyric_filepath)
                if maybe_lyric_text is not None:
                    with open(lyric_filepath, 'wt', encoding=configuration.TEXT_ENCODING) as lyric_file:
                        lyric_file.write(maybe_lyric_text)
                    audio.lyrics_filepath = lyric_filepath
                else:
                    audio.lyrics_filepath = None
            except TypeError:
                audio.lyrics_filepath = None
