import time
from threading import Lock

import pylrc
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

def show_lyrics(audio: Audio, audio_progression_in_sec: float):
    ''' Print the lyric if the music is playing
    @param audio: Audio: audio that can contain the lyric to show
    @param audio_progression_in_sec: float: the timing the audio is currently playing at
    '''
    SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC = 1
    REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC = 0.1
    if audio.lyrics_filepath is None:
        print("Warning: there is no lyrics prepared for the audio.")
        return
    starting_time_in_sec = time.time() - audio_progression_in_sec
    with open(audio.lyrics_filepath, "rt", encoding=configuration.TEXT_ENCODING) as lyric_file:
        lyric_text: pylrc.classes.Lyrics = pylrc.parse(lyric_file.read())
        for lyric_line in lyric_text:
            time_passed_from_start = time.time() - starting_time_in_sec
            while time_passed_from_start < lyric_line.time - REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC - SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC:
                time.sleep(REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC)
                time_passed_from_start = time.time() - starting_time_in_sec
            print(lyric_line.text)
