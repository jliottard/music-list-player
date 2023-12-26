import vlc
from audio import playlist

class AudioPlayer:
    def __init__(self, playlist: playlist.Playlist):
        self.player = vlc.Instance()    
        self.media_list = self.player.media_list_new()
        self.playlist = playlist
        for audio in self.playlist.audios:
            self.media_list.add_media(self.player.media_new(audio.filepath))
        self.audio_list_player = self.player.media_list_player_new()
        self.audio_list_player.set_media_list(self.media_list)

    def play(self):
        self.audio_list_player.play()

    def pause(self):
         self.audio_list_player.pause()

    def stop(self):
        self.audio_list_player.stop()

    def next(self):
        self.playlist.current_audio_index += 1
        self.audio_list_player.next()

    def is_playing(self) -> bool:
        return self.audio_list_player.is_playing()

