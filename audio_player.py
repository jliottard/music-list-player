import vlc

class Audio:
    def __init__(self, name: str, filepath: str):
        self.name = name
        self.filepath = filepath

class Playlist:
    def __init__(self):
        self.audios: list[Audio] = []
        self.current_audio_index = 0
    
    def current_audio(self) -> Audio:
        # error: it returns None if the audio index does not match an audio
        if self.current_audio_index >= len(self.audios):
            return None
        return self.audios[self.current_audio_index]

class AudioPlayer:
    def __init__(self, playlist: Playlist):
        self.playlist = playlist
        self.player = self.new_player_for_current_audio()
    
    def replace(self, playlist: Playlist):
        self.playlist = playlist
        self.player = self.new_player_for_current_audio()

    def new_player_for_current_audio(self):
        # error: it returns None is there is no current audio in the playlist
        current_audio = self.playlist.current_audio()
        if current_audio is None:
            return None
        return vlc.MediaPlayer(current_audio.filepath)

    def play(self):
        # exception: raise an error if there is no current audio in playlist
        self.player = self.new_player_for_current_audio()
        if self.player is None:
            raise Exception("no current audio in playlist")
        self.player.play()

    def pause(self):
        # exception: raise an error when the AudioPlayer instance does not have
        # a instanciate player
        if self.player is None:
            raise Exception("vlc player not instanciated")
        self.player.pause()

    def stop(self):
        # exception: raise an error when the AudioPlayer instance does not have
        # a instanciate player
        if self.player is None:
            raise Exception("vlc player not instanciated")
        self.player.stop()

    def next(self):
        # exception: raise an error if there is no next audio in the playlist
        self.player.stop()
        if self.playlist.current_audio_index >= len(self.playlist.audios) - 1:
            raise Exception("End of the playlist")
        self.playlist.current_audio_index += 1
        self.play()
