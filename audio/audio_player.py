import random
import time
import vlc
from audio.audio import Audio
from audio.playlist import Playlist
from audio.play_mode import PlayMode, translate_play_mode

class AudioPlayer:
    AUDIO_VOLUME_BASE = 100

    def __init__(self, playlist: Playlist, volume: int):
        ''' Instanciate the AudioPlayer object
        @param playlist: Playlist: can be empty but not None
        @param volume: int: the player's sound volume from 0 to 100 (percentage).
        '''
        # Data
        self.playlist = playlist
        self.play_mode: PlayMode = PlayMode.ONE_PASS
        self.volume = volume
        # Actors
        self.player: vlc.Instance = vlc.Instance()
        self.media_list: vlc.MediaList = self.player.media_list_new()
        self.audio_list_player: vlc.MediaListPlayer = self.player.media_list_player_new()
        # Actors' modifiers
        self._overwrite_playlist(playlist)
        self.audio_list_player.set_playback_mode(translate_play_mode(self.play_mode))
        self.set_volume(volume)

    def append_audio_to_playlist(self, audio: Audio):
        ''' Add the audio to the playlist and load it to the media list
        @param: audio: Audio: instanciated audio with an existing file path
        '''
        self.playlist.audios.append(audio)
        self.media_list.add_media(self.player.media_new(audio.filepath))

    def _overwrite_playlist(self, playlist: Playlist):
        self.playlist = Playlist()
        for audio in playlist.audios:
            self.append_audio_to_playlist(audio)
        self.audio_list_player.set_media_list(self.media_list)

    def play(self):
        self.audio_list_player.play()

    def pause(self):
        self.audio_list_player.set_pause(1)

    def resume(self):
        self.audio_list_player.set_pause(0)

    def stop(self):
        self.audio_list_player.stop()

    def next(self):
        self.audio_list_player.next()

    def is_playing(self) -> bool:
        return self.audio_list_player.is_playing()

    def shuffle(self):
        ''' Rearrange the order of the playlist. The state of the played audio can be late to be updated '''
        random.shuffle(self.playlist.audios)
        self._overwrite_playlist(self.playlist)

    def get_index_of_audio(self, searched_audio: Audio) -> int:
        for index, playlist_audio in enumerate(self.playlist.audios):
            if searched_audio == playlist_audio:
                return index
        return -1

    def get_playing_audio_index(self) -> int:
        ''' Return None if there is no playing audio '''
        for media_index, media in enumerate(self.media_list):
            if media.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
                return media_index
        return None

    def get_next_audio_index(self) -> int:
        """
        Get the next index from the playing audio in the player's playlist. Assume the playlist loops.
        @return: None if there is no playing audio or the current audio is the last while the play mode is one pass
        """
        maybe_playing_audio_index = self.get_playing_audio_index()
        if maybe_playing_audio_index is None:
            return None
        next_audio_index = (maybe_playing_audio_index + 1) % len(self.playlist.audios)
        match self.get_play_mode():
            case PlayMode.PLAYLIST_LOOP:
                return next_audio_index
            case PlayMode.ONE_PASS:
                if maybe_playing_audio_index == len(self.playlist.audios) - 1:
                    return None
                return next_audio_index
            case _:
                return None

    def get_playing_audio(self) -> Audio:
        """ Return None if there is no playing audio """
        maybe_audio_index = self.get_playing_audio_index()
        if maybe_audio_index is None:
            return None
        return self.playlist.audios[maybe_audio_index]

    def get_next_audio(self) -> Audio:
        """ Return None if there is no playing audio or the play mode is one pass and the current audio is the last """
        maybe_next_audio_index = self.get_next_audio_index()
        if maybe_next_audio_index is None:
            return None
        return self.playlist.audios[maybe_next_audio_index]

    def set_play_mode(self, mode: PlayMode):
        self.play_mode = mode
        self.audio_list_player.set_playback_mode(translate_play_mode(self.play_mode))

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
        return self.audio_list_player.play_item_at_index(index) == 0

    def get_volume(self) -> int:
        ''' Return the volume percentage '''
        media_player = self.audio_list_player.get_media_player()
        volume = media_player.audio_get_volume()
        media_player.release()
        return volume

    def set_volume(self, volume_percentage: int):
        ''' Set the player's volume 
        @param volume_percentage: int: the volume to be set from 0 to twice the <AudioPlayer.AUDIO_VOLUME_BASE>'''
        self.volume = min(volume_percentage, AudioPlayer.AUDIO_VOLUME_BASE*2)
        media_player = self.audio_list_player.get_media_player()
        media_player.audio_set_volume(self.volume)
        media_player.release()

    def get_playing_audio_duration_in_ms(self) -> float:
        ''' Return the time duration of the current playing audio)
        @return float
        '''
        while self.get_playing_audio() is None:
            time.sleep(1)

        playing_media = self.media_list[self.get_playing_audio_index()]
        playing_media.parse()
        return playing_media.get_duration()

    def get_audio_progress_time_in_sec(self) -> float:
        ''' Return the current playing audio time progression '''
        while self.get_playing_audio() is None:
            time.sleep(1)
        time_in_ms = self.audio_list_player.get_media_player().get_time()
        return time_in_ms * (10 ** (-3))
