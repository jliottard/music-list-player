from enum import Enum
from vlc import PlaybackMode

class PlayMode(Enum):
    ONE_PASS = PlaybackMode.default, "one pass"
    PLAYLIST_LOOP = PlaybackMode.loop, "playlist loop"

    def __str__(self) -> str:
        return self.value[1]

def from_string(string: str) -> PlayMode:
    for mode in PlayMode:
        if string == str(mode):
            return mode
    raise ValueError("Not matching play mode.")

def translate_play_mode(mode: PlayMode) -> PlaybackMode:
    return mode.value[0]
