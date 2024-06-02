import random
import time
import vlc
from audio.audio import Audio
from audio.playlist import Playlist
from audio.play_mode import PlayMode, translate_play_mode

class AudioPlayer:
    AUDIO_VOLUME_BASE = 100
    COEF_MS_TO_SEC = 1e-3
    COEF_SEC_TO_MS = 1000

    def __init__(self, playlist: Playlist, volume: int):
        """ Instanciate the AudioPlayer object
        @param playlist: Playlist: can be empty but not None
        @param volume: int: the player's sound volume from 0 to 100 (percentage).
        """
        # Data
        self.playlist = playlist
        self.play_mode: PlayMode = PlayMode.ONE_PASS
        self.volume = volume
        # Actors
        self.instance: vlc.Instance = vlc.Instance()
        self.media_list: vlc.MediaList = None
        self.media_list_player: vlc.MediaListPlayer = self.instance.media_list_player_new()
        # Actors' modifiers
        self._overwrite_playlist(playlist)
        self.media_list_player.set_playback_mode(translate_play_mode(self.play_mode))
        self.set_volume(volume)

    def append_audio_to_player_playlist(self, audio: Audio):
        """ Add the audio to the playlist and load it to the media list
        @param: audio: Audio: instanciated audio with an existing file path
        """
        self.playlist.audios.append(audio)
        self.media_list.add_media(self.instance.media_new(audio.filepath))

    def _overwrite_playlist(self, playlist: Playlist):
        self.playlist = Playlist()
        if self.media_list is not None:
            self.media_list.release()
        self.media_list = self.instance.media_list_new()
        for audio in playlist.audios:
            self.append_audio_to_player_playlist(audio)
        self.media_list_player.set_media_list(self.media_list)

    def play(self):
        self.media_list_player.play()

    def pause(self):
        self.media_list_player.set_pause(1)

    def resume(self):
        self.media_list_player.set_pause(0)

    def stop(self):
        self.media_list_player.stop()

    def next(self):
        self.media_list_player.next()

    def is_playing(self) -> bool:
        return self.media_list_player.is_playing()

    def shuffle(self):
        """ Rearrange the order of the playlist. The state of the played audio can be late to be updated """
        random.shuffle(self.playlist.audios)
        self._overwrite_playlist(self.playlist)

    def get_index_of_audio(self, searched_audio: Audio) -> int:
        for index, playlist_audio in enumerate(self.playlist.audios):
            if searched_audio == playlist_audio:
                return index
        return -1

    def get_playing_audio_index(self) -> int:
        '''Get the index of the playing audio or None if there is no media being played
        It is assumed that one audio file is loaded only once in the AudioPlayer's playlist,
            so there is no Audios that share the same audio file path.
        @return int | None
        '''
        maybe_media_player: vlc.MediaPlayer = self.media_list_player.get_media_player()
        if maybe_media_player is not None:
            maybe_media: vlc.Media = maybe_media_player.get_media()
            if maybe_media is None:
                maybe_media_player.release()
                return None
        else:
            return None
        for media_index, media in enumerate(self.media_list):
            if media.get_mrl() == maybe_media.get_mrl():
                maybe_media_player.release()
                return media_index
        maybe_media_player.release()
        return None

    def get_next_audio_index(self) -> int:
        """
        Get the next index from the playing audio in the player's playlist. Assume the playlist loops.
        @return: None if there is no playing audio or the current audio is the last while the play mode is one pass
        """
        maybe_playing_audio_index = self.get_playing_audio_index()
        if maybe_playing_audio_index is None:
            return None
        playing_audio_index: int = maybe_playing_audio_index
        next_audio_index = (playing_audio_index + 1) % len(self.playlist.audios)
        match self.get_play_mode():
            case PlayMode.PLAYLIST_LOOP:
                return next_audio_index
            case PlayMode.ONE_PASS:
                if playing_audio_index == len(self.playlist.audios) - 1:
                    return None
                return next_audio_index
            case _:
                return None

    def get_playing_audio(self) -> Audio | None:
        """ Return None if there is no playing audio """
        maybe_audio_index = self.get_playing_audio_index()
        if maybe_audio_index is None:
            return None
        audio_index: int = maybe_audio_index
        return self.playlist.audios[audio_index]

    def get_next_audio(self) -> Audio | None:
        """ Return None if there is no playing audio or the play mode is one pass and the current audio is the last """
        maybe_next_audio_index = self.get_next_audio_index()
        if maybe_next_audio_index is None:
            return None
        next_audio_index: int = maybe_next_audio_index
        return self.playlist.audios[next_audio_index]

    def set_play_mode(self, mode: PlayMode):
        self.play_mode = mode
        self.media_list_player.set_playback_mode(translate_play_mode(self.play_mode))

    def get_play_mode(self) -> PlayMode:
        return self.play_mode

    def play_audio_at_index(self, index: int) -> bool:
        """
        Returns:
         - True on success
         - False on Failure, if the index is not found
        """
        if index >= len(self.playlist.audios):
            return False
        return self.media_list_player.play_item_at_index(index) == 0

    def get_volume(self) -> int:
        """ Return the volume percentage """
        media_player: vlc.MediaPlayer = self.media_list_player.get_media_player()
        volume = media_player.audio_get_volume()
        media_player.release()
        return volume

    def set_volume(self, volume_percentage: int):
        """ Set the player's volume 
        @param volume_percentage: int: the volume to be set from 0 to twice the 
            <AudioPlayer.AUDIO_VOLUME_BASE>
        """
        self.volume = min(volume_percentage, AudioPlayer.AUDIO_VOLUME_BASE*2)
        media_player: vlc.MediaPlayer = self.media_list_player.get_media_player()
        media_player.audio_set_volume(self.volume)
        media_player.release()

    def get_playing_audio_duration_in_sec(self) -> float | None:
        """ Return the time duration of the playing audio
        @return float or None if there is no playing audio
        """
        maybe_playing_audio_index = self.get_playing_audio_index()
        if maybe_playing_audio_index is None:
            return None
        playing_audio_index: int = maybe_playing_audio_index
        playing_media: vlc.Media = self.media_list[playing_audio_index]
        playing_media.parse()   # NOTE: parse method is deprecated but parse_with_options does not work
        return playing_media.get_duration() * AudioPlayer.COEF_MS_TO_SEC

    def get_audio_progress_time_in_sec(self) -> float | None:
        """ Return the current playing audio time progression
        @return float or None if there is no playing audio
        """
        if not self.is_playing():
            return None
        media_player: vlc.MediaPlayer = self.media_list_player.get_media_player()
        time_in_ms = media_player.get_time()
        media_player.release()
        return time_in_ms * AudioPlayer.COEF_MS_TO_SEC

    def set_current_audio_time(self, time_in_sec: int):
        """ Set the current audio timeline
        Do nothing if the given time in out of range of the audio length
        Do nothing if there is not playing media
        @param time_in_sec: int
        """
        maybe_audio_time_in_sec = self.get_playing_audio_duration_in_sec()
        if maybe_audio_time_in_sec is None:
            return
        audio_time_in_sec: float = maybe_audio_time_in_sec
        if not 0 <= time_in_sec <= audio_time_in_sec:
            return
        time_in_ms: int = time_in_sec * AudioPlayer.COEF_SEC_TO_MS
        media_player: vlc.MediaPlayer = self.media_list_player.get_media_player()
        media_player.set_time(time_in_ms)
        media_player.release()
