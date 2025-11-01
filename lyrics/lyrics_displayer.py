import time
from threading import Thread

import pylrc

from app import file_management
from app.config.configuration import TEXT_ENCODING
from app.interface import Interface
from app.message_priority import MessagePriority
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
        if maybe_audio is None:
            return False
        audio: Audio = maybe_audio
        return audio.lyrics_filepath is not None and file_management.is_file_in_cache(audio.lyrics_filepath)

    @staticmethod
    def get_lyric_text(audio: Audio) -> pylrc.classes.Lyrics:
        """Return the lyric text contents of the audio"""
        lyrics = None
        with open(audio.lyrics_filepath, "rt", encoding=TEXT_ENCODING) as lyric_file:
            lyrics: pylrc.classes.Lyrics = pylrc.parse(lyric_file.read())
        return lyrics

    def show_lyrics(self, user_interface: Interface):
        """Print the lyric if the music is playing
        @param user_interface: Inteface
        """
        def _is_progress_before_lyric_time(lyric_line: pylrc.classes.LyricLine) -> bool:
            return self.player.get_audio_progress_time_in_sec() < lyric_line.time - REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC - SHOW_LYRICS_IN_ADVANCE_DURATION_IN_SEC

        def _has_audio_with_lyrics_changed() -> bool:
            return self.player.get_playing_audio() is not None and self.displayed_lyric_audio != self.player.get_playing_audio()

        user_interface.mute_message(MessagePriority.INFO)
        user_interface.mute_message(MessagePriority.WARNING)
        while self.are_lyrics_on:
            maybe_base_audio = self.player.get_playing_audio()
            if self.are_audio_lyrics_available(maybe_base_audio):
                base_audio: Audio = maybe_base_audio
                if _has_audio_with_lyrics_changed():
                    user_interface.request_output_to_user(
                        f"Lyrics: \"{base_audio.name_without_extension}\" audio's lyrics:",
                        MessagePriority.LYRICS
                    )
                    self.displayed_lyric_audio = base_audio
                    lyrics: pylrc.classes.Lyrics = LyricsDisplayer.get_lyric_text(self.displayed_lyric_audio)
                    for lyric_line in lyrics:
                        if self.are_lyrics_on:
                            while self.player.get_audio_progress_time_in_sec() is not None and not _has_audio_with_lyrics_changed() and _is_progress_before_lyric_time(lyric_line):
                                time.sleep(REFRESH_NEXT_LYRIC_TIME_CHECK_IN_SEC)
                            if not self.are_lyrics_on or _has_audio_with_lyrics_changed():
                                break
                            if self.player.is_playing():
                                user_interface.request_output_to_user(
                                    "\t" + lyric_line.text,
                                    MessagePriority.LYRICS
                                )
                        else:
                            break
            else:
                time.sleep(HALT_TIME_BEFORE_TRYING_TO_GET_PLAYING_AUDIO_IN_SEC)
        user_interface.unmute_message(MessagePriority.INFO)
        user_interface.unmute_message(MessagePriority.WARNING)
