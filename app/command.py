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
            Command.IMPORT: "load the default playlist's musics. Alternatively load a custom playlist from the configuration: \"import <profile_name>\"",
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

def parse_command(command_input: str) -> list:
    # Parse the inputed by user command
    # Return:
    # - a list of the command arguments with the first argument as a Command element
    # - None if the command is not recognized
    def is_not_empty_string(e: str) -> bool:
        return e != ""
    args = list(filter(is_not_empty_string, command_input.split(" ")))
    if len(args) == 0:
        return None
    first_argument = args[0]
    for command_enum in Command:
        if first_argument == command_enum.value:
            args[0] = command_enum
    if isinstance(args[0], str):
        return None
    return args