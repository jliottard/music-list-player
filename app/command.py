from enum import Enum

from app.config.configuration_keyword import ConfigurationKeyword
from app.message_priority import MessagePriority
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
    VOLUME = "volume"
    LYRIC = "lyric"
    MOVE = "move"
    PROFILE = "profile"
    MUTE = "mute"
    UNMUTE = "unmute"

    def __str__(self) -> str:
        return self.value

    def help(self):
        """ Provide a help description for the command instance """
        command_help = {
            Command.HELP: "show the details of the commands' usages",
            Command.QUIT: "exit the application",
            Command.IMPORT: f"load all the playlist's musics by default. Alternatively load a tag-based-playlist from the playlist: \"import #<tag_name>\". While the audio are loading, you can use command as usual if the configuration's setting \"{ConfigurationKeyword.USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT.value}\" is set to 'false'.",
            Command.LIST: "show the playlist's musics",
            Command.PLAY: "play first audio by default . If prefixed by the playlist's audio index (one argument), play the corresponding audio: \"play <i>\". If the command is prefixed with at least 2 arguments as audio's name, it will try to play the matching audio: \"play <first_audio_name_part> <second_audio_name_part> [<other_audio_name_part>]*\"",
            Command.NEXT: "skip the current music to play the next one in the playlist",
            Command.STOP: "halt the audio",
            Command.PAUSE: "pause the audio",
            Command.RESUME : "resume the paused audio",
            Command.SHUFFLE: "shuffle the order of the musics and restart the played song",
            Command.MODE: "show the current play mode, or with argument(s), set the play mode accordingly: {}".format(
                [str(mode) for mode in PlayMode]
            ),
            Command.VOLUME: "show current volume. Alternatively, increase or decrease the volume by a percentage: \"volume up/down <percentage>\"",
            Command.LYRIC: "show the lyrics of the played song, or if prefixed by 'on' or 'off' turn on or off accordingly the lyrics display.",
            Command.MOVE: "move the play moment of the current audio (in second): \"move 10.0\" : move the time of the audio to the 10th second.",
            Command.PROFILE: "change the profile, or without arguments show the current profile : \"profile default\": change the profile to the \"default-profile\" from the configuration file",
            Command.MUTE : "mute the messages of one priority : mute <{}>".format(
                [str(prio) for prio in MessagePriority]
            ),
            Command.UNMUTE : "unmute the messages of one priority : unmute <{}>".format(
                [str(prio) for prio in MessagePriority]
            )
        }
        return command_help[self]

def parse_command(command_input: str) -> list:
    # Parse the inputed by user command
    # Return:
    # - a list of the command arguments with the first argument as a Command element
    # - None if the command is not recognized
    def is_not_empty_string(string: str) -> bool:
        return string != ""
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
