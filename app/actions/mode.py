from app.cannot_find_a_match_error import CannotFindAMatchError
from app.interface import Interface
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
            MODES = [str(mode) for mode in PlayMode]
            mode_index = match_string_among_strings(" ".join(args[1:]), MODES)
            player.set_play_mode(from_string(MODES[mode_index]))
        except CannotFindAMatchError:
            user_interface.request_output_to_user(f"Cannot find a matching mode with \"{args[1:]}\".")
        else:
            user_interface.request_output_to_user(f"Setting play mode as {player.get_play_mode()}.")
    else:
        user_interface.request_output_to_user(f"Current play mode is {player.get_play_mode()}.")
