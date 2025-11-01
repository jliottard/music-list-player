''' "mode" command functionality '''

from app.cannot_find_a_match_error import CannotFindAMatchError
from app.interface import Interface
from app.message_priority import MessagePriority
from app.search import match_string_among_strings
from audio.audio_player import AudioPlayer
from audio.play_mode import PlayMode, from_string

def request_mode(args: list, player: AudioPlayer, user_interface: Interface) -> None:
    """Set the playmode of the playlist according to the arguments
    @param args: List[Command, str...]
    @param player: AudioPlayer
    @paramm user_interface: Interface
    """
    if len(args) >= 2:
        try:
            modes = [str(mode) for mode in PlayMode]
            mode_index = match_string_among_strings(" ".join(args[1:]), modes)
            player.set_play_mode(from_string(modes[mode_index]))
        except CannotFindAMatchError:
            user_interface.request_output_to_user(f"Warning: Cannot find a matching mode with \
             \"{args[1:]}\".", MessagePriority.WARNING)
        else:
            user_interface.request_output_to_user(f"Info: Setting play mode as \
             {player.get_play_mode()}.", MessagePriority.INFO)
    else:
        user_interface.request_output_to_user(
            f"Info: Current play mode is {player.get_play_mode()}.", MessagePriority.INFO
        )
