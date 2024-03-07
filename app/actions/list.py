from audio.audio_player import AudioPlayer
from audio.playlist import Playlist

def print_list(player: AudioPlayer) -> None:
    """ Print the list of musics in the playlist"""
    print("Music list:")
    maybe_played_audio = player.get_playing_audio()
    for index, audio in enumerate(player.playlist.audios):
        is_playing_status = "\t\t (currently playing)" if maybe_played_audio is not None and audio == maybe_played_audio else ""
        extra_information = "(lyrics available)" if audio.lyrics_filepath is not None else ""
        print(f"- ({index}) {audio.name} {extra_information} {is_playing_status}")
