import time
from threading import Thread

import pylrc

from app import configuration, file_management
from app.interface import Interface
from audio.audio import Audio
from audio.audio_player import AudioPlayer

# Constants
SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC = 1
REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC = 0.1
HALT_TIME_BEFORE_TRYING_TO_GET_PLAYING_AUDIO_IN_SEC = 2

# Class
class LyricsDisplayer:
    """Lyric displaying class"""
    def __init__(self, player: AudioPlayer, user_interface: Interface):
        self.are_lyrics_on: bool = False
        self.lyric_thread: Thread = None
        self.player: AudioPlayer = player
        self.user_interface: Interface = user_interface
        self.displayed_lyric_audio: Audio | None = None

    def __del__(self):
        self.set_lyrics(False)

    def set_lyrics(self, active: bool):
        """Active or deactivate the lyrics printing of the playing audio
        @param active bool: if True, the lyric are displayed
        """
        self.are_lyrics_on = active
        if self.are_lyrics_on:
            self.lyric_thread = Thread(
                target=self.show_lyrics,
                args=[self.user_interface],
                daemon=True
            )
            self.lyric_thread.start()
        else:
            if self.lyric_thread is not None:
                self.lyric_thread.join()

    def are_audio_lyrics_available(self, maybe_audio: Audio | None) -> bool:
        """Return True if the audio is valid and the audio refers to a lyric file"""
        return maybe_audio is not None and maybe_audio.lyrics_filepath is not None and file_management.is_file_in_cache(maybe_audio.lyrics_filepath)

    def get_lyric_text(self, audio: Audio) -> pylrc.classes.Lyrics:
        """Return the lyric text contents of the audio"""
        lyric_text = None
        with open(audio.lyrics_filepath, "rt", encoding=configuration.TEXT_ENCODING) as lyric_file:
            lyric_text: pylrc.classes.Lyrics = pylrc.parse(lyric_file.read())
        return lyric_text

    def show_lyrics(self, user_interface):
        """Print the lyric if the music is playing
        @param user_interface: Inteface
        """
        while self.are_lyrics_on:
            maybe_base_audio = self.player.get_playing_audio()
            if self.are_audio_lyrics_available(maybe_base_audio):
                lyric_text: pylrc.classes.Lyrics = self.get_lyric_text(maybe_base_audio)
                self.displayed_lyric_audio = maybe_base_audio
                last_lyric = lyric_text[-1]
                user_interface.request_output_to_user(f"Info: \"{self.displayed_lyric_audio.name}\" audio's lyrics:")
                for lyric_line in lyric_text:
                    if self.are_lyrics_on:
                        maybe_progress_time_in_sec = self.player.get_audio_progress_time_in_sec()
                        has_audio_changed = self.displayed_lyric_audio != self.player.get_playing_audio()
                        while maybe_progress_time_in_sec is not None and not has_audio_changed and maybe_progress_time_in_sec < lyric_line.time - REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC - SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC:
                            time.sleep(REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC)
                            maybe_progress_time_in_sec = self.player.get_audio_progress_time_in_sec()
                            has_audio_changed = self.displayed_lyric_audio != self.player.get_playing_audio()
                        if maybe_progress_time_in_sec is not None:
                            was_last_lyric_reached = maybe_progress_time_in_sec > last_lyric.time
                            if was_last_lyric_reached:
                                break
                        if not self.are_lyrics_on or has_audio_changed:
                            break
                        if self.player.is_playing():
                            user_interface.request_output_to_user("\t" + lyric_line.text)
                    else:
                        break
            else:
                time.sleep(HALT_TIME_BEFORE_TRYING_TO_GET_PLAYING_AUDIO_IN_SEC)
