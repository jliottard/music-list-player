from app.interface import Interface
from audio.audio_player import AudioPlayer

def print_list(player: AudioPlayer, user_interface: Interface) -> None:
    """ Print the list of musics in the playlist"""
    user_interface.request_output_to_user("Music list:")
    maybe_played_audio = player.get_playing_audio()
    for index, audio in enumerate(player.playlist.audios):
        audio_info = ""
        if maybe_played_audio is not None and audio == maybe_played_audio:
            audio_info = Interface.playing_audio_status(player)
            is_playing_status = "\t\t (currently playing)"
        else:
            audio_info = audio.name_without_extension
            is_playing_status = ""
        extra_information = "(lyrics available)" if audio.lyrics_filepath is not None else ""
        user_interface.request_output_to_user(
            f"- ({index}) {audio_info} {extra_information} {is_playing_status}"
        )
