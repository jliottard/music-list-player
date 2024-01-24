import random
from typing import List, Tuple
import vlc
from audio import playlist, audio

class AudioPlayer:
    def __init__(self, playlist: playlist.Playlist):
        self.playlist = playlist
        self.player, self.media_list, self.audio_list_player = self.__set_media_player(self.playlist.audios)   
    
    def __set_media_player(self, audio_playlist: List[audio.Audio]) -> Tuple[vlc.Instance, vlc.MediaList, vlc.Instance.media_list_new]:
        player: vlc.Instance = vlc.Instance()
        media_list: vlc.MediaList = player.media_list_new()
        for audio in audio_playlist:
            media_list.add_media(player.media_new(audio.filepath))
        audio_list_player: vlc.MediaListPlayer = player.media_list_player_new()
        audio_list_player.set_media_list(media_list)
        return player, media_list, audio_list_player
    
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
        # Description: rearrange the order of the playlist. The state of the played audio can be late to be up to date
        random.shuffle(self.playlist.audios)
        self.player, self.media_list, self.audio_list_player = self.__set_media_player(self.playlist.audios)

    def play_audio_at_index(self, index: int):
        self.audio_list_player.play_item_at_index(index)

    def get_index_of_audio(self, searched_audio: audio.Audio) -> int:
        for index, playlist_audio in enumerate(self.playlist.audios):
            if searched_audio == playlist_audio:
                return index
        return -1

    def get_playing_audio_index(self) -> int:
        # Return None if there is no playing audio
        for media_index, media in enumerate(self.media_list):
            if media.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
                return media_index
        return None
    
    def get_playing_audio(self) -> audio.Audio:
        # Return None if there is no playing audio
        maybe_audio_index = self.get_playing_audio_index()
        if maybe_audio_index is None:
            return None
        return self.playlist.audios[maybe_audio_index]

    def set_default(self):
        self.audio_list_player.set_playback_mode(vlc.PlaybackMode.default)

    def set_loop(self):
        self.audio_list_player.set_playback_mode(vlc.PlaybackMode.loop)

    def play_audio_at_index(self, index: int) -> bool:
        # Returns:
        # - True on success
        # - False on Failure, if the index is not found
        return self.audio_list_player.play_item_at_index(index) == 0
