from audio import audio

class Playlist:
    def __init__(self):
        self.audios: list[audio.Audio] = []
        self.current_audio_index = 0
    
    def current_audio(self) -> audio.Audio:
        # error: it returns None if the audio index does not match an audio
        if self.current_audio_index >= len(self.audios):
            return None
        return self.audios[self.current_audio_index]
