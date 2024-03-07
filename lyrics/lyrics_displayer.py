import time
from threading import Thread

import pylrc

from app import configuration
from audio.audio_player import AudioPlayer
from audio.audio import Audio

# Constants
SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC = 1
REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC = 0.1

# Class
class LyricsDisplayer:
    '''Lyric displaying class'''
    def __init__(self, player: AudioPlayer):
        self.is_displaying = False
        self.lyric_thread = None
        self.player = player

    def __del__(self):
        self.set_lyrics(False)

    def set_lyrics(self, active: bool):
        '''Active or deactivate the lyrics printing of the playing audio
        @param active bool: if True, the lyric are displayed
        '''
        self.is_displaying = active
        if self.is_displaying:
            maybe_audio = self.player.get_playing_audio()
            if maybe_audio is None:
                print("Warning: there is no playing audio, so there is no lyrics to display.")
                return
            if maybe_audio.lyrics_filepath is None:
                print("Warning: the playing audio has no filepath location.")
                return
            audio_progression_in_sec = self.player.get_audio_progress_time_in_sec()
            self.lyric_thread = Thread(
                target=self.show_lyrics,
                args=(maybe_audio, audio_progression_in_sec),
                daemon=True
            )
            self.lyric_thread.start()
        else:
            if self.lyric_thread is not None:
                self.lyric_thread.join()

    def show_lyrics(self, audio: Audio, audio_progression_in_sec: float):
        ''' Print the lyric if the music is playing
        @param audio: Audio: audio that can contain the lyric to show
        @param audio_progression_in_sec: float: the timing the audio is currently playing at
        '''
        if audio.lyrics_filepath is None:
            print("Warning: there is no lyrics prepared for the audio.")
            return
        starting_time_in_sec = time.time() - audio_progression_in_sec
        with open(audio.lyrics_filepath, "rt", encoding=configuration.TEXT_ENCODING) as lyric_file:
            lyric_text: pylrc.classes.Lyrics = pylrc.parse(lyric_file.read())
            for lyric_line in lyric_text:                
                if self.is_displaying:
                    time_passed_from_start = time.time() - starting_time_in_sec
                    while time_passed_from_start < lyric_line.time - REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC - SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC:
                        time.sleep(REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC)
                        time_passed_from_start = time.time() - starting_time_in_sec
                    print(lyric_line.text)
                else:
                    break
