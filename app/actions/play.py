from app.cannot_find_a_match_error import CannotFindAMatchError
from app.interface import Interface
from app.search import match_string_among_strings
from audio.audio_player import AudioPlayer

def play(args: list, player: AudioPlayer, user_interface: Interface) -> None:
    """ Play the music according to the args """
    if len(args) == 1:
        player.play()
    if len(args) == 2:
        try:
            second_argument = args[1]
            audio_index = int(second_argument)
        except ValueError:
            user_interface.request_output_to_user(f"Unexpected argument provided: \"{second_argument}\", it was expected to be the index of the audio in the playlist (integer).")
            return
        if not player.play_audio_at_index(audio_index):
            user_interface.request_output_to_user(f"Cannot find the \"{audio_index}\" index in the playlist.")
            return
    if len(args) > 2:
        try:
            audio_name_to_play = " ".join(args[1:])
        except ValueError:
            user_interface.request_output_to_user(f"Unexpected name provided: \"{args[1:]}\", it was expected to be a audio name (string).")
            return
        try:
            audio_to_play_index = match_string_among_strings(audio_name_to_play, player.playlist.names())
        except CannotFindAMatchError:
            user_interface.request_output_to_user(f"Cannot find a matching audio with \"{audio_name_to_play}\".")
            return
        else:
            if not player.play_audio_at_index(audio_to_play_index):
                user_interface.request_output_to_user(f"Audio match found but cannot find its \"{audio_to_play_index}\" index in the playlist.")
            return
    maybe_played_audio = player.get_playing_audio()
    if maybe_played_audio is None:
        user_interface.request_output_to_user("Playing..")
    else:
        user_interface.request_output_to_user(f"Playing \"{maybe_played_audio.name}\".")
