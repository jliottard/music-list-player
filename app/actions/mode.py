from app.search import match_string_among_strings
from app.cannot_find_a_match_error import CannotFindAMatchError
from audio.audio_player import AudioPlayer
from audio.play_mode import PlayMode, from_string

def define_mode(args: list, player: AudioPlayer) -> None:
    """Set the playmode of the playlist according to the arguments"""
    if len(args) >= 2:
        try:
            MODES = [str(mode) for mode in PlayMode]
            mode_index = match_string_among_strings(" ".join(args[1:]), MODES)
            player.set_play_mode(from_string(MODES[mode_index]))
        except CannotFindAMatchError:
            print(f"Cannot find a matching mode with \"{args[1:]}\".")
        else:
            print(f"Setting play mode as {player.get_play_mode()}.")
    else:
        print(f"Current play mode is {player.get_play_mode()}.")
