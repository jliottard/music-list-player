from enum import Enum
from audio.play_mode import PlayMode

class Command(Enum):
    HELP = "help"
    QUIT = "quit"
    IMPORT = "import"
    LIST = "list"
    PLAY = "play"
    NEXT = "next"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    SHUFFLE = "shuffle"
    MODE = "mode"

    def __str__(self) -> str:
        return self.value
    
    def help(self):
        command_help = {
            Command.HELP: "show the details of the commands' usages",
            Command.QUIT: "exit the application",
            Command.IMPORT: "download the musics using Internet connection and set the playlist",
            Command.LIST: "show the playlist's musics",
            Command.PLAY: "play first audio by default or if prefixed by the playlist's audio index, play the corresponding audio: \"play <i>\"",
            Command.NEXT: "skip the current music to play the next one in the playlist",
            Command.STOP: "halt the audio",
            Command.PAUSE: "pause the audio",
            Command.RESUME : "resume the paused audio",
            Command.SHUFFLE: "shuffle the order of the musics and restart the played song",
            Command.MODE: "show the current play mode, or with argument(s), set the play mode accordingly: {}".format(
                [str(mode) for mode in PlayMode]
            ),
        }
        return command_help[self]
