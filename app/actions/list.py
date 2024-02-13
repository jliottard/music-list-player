from audio.audio_player import AudioPlayer
from audio.playlist import Playlist

def print_list(player: AudioPlayer) -> None:
    """ Print the list of musics in the playlist"""
    print("Music list:")
    maybe_played_audio = player.get_playing_audio()
    for index, audio in enumerate(player.playlist.audios):
        if maybe_played_audio is not None and audio == maybe_played_audio:
            print(f"- ({index}) {audio.name} \t\t (currently playing)")
        else:
            print(f"- ({index}) {audio.name}")
