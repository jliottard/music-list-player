from typing import List
from audio import audio

class Playlist:
    def __init__(self):
        self.audios: list[audio.Audio] = []

    def names(self) -> List[str]:
        # Return the name of the audios in order to the playlist
        return [audio.name for audio in self.audios]
