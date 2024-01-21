from enum import Enum

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
    
    def help(self):
        command_help = {
            Command.HELP: "show the details of the commands' usages",
            Command.QUIT: "exit the application",
            Command.IMPORT: "download the musics using Internet connection and set the playlist",
            Command.LIST: "show the playlist's musics",
            Command.PLAY: "play the playlist",
            Command.NEXT: "skip the current music to play the next one in the playlist",
            Command.STOP: "halt the audio",
            Command.PAUSE: "toggle the audio",
            Command.RESUME : "resume the paused audio",
            Command.SHUFFLE: "shuffle the order of the musics and restart the played song"
        }
        return command_help[self]

