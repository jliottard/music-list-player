import os

from audio.audio import Audio
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist

def clean_terminal() -> None:
    ''' Clean the Unix terminal '''
    os.system('tput reset')

def status_information_str(player: AudioPlayer) -> str:
    ''' Return the player basics information such as playing song and upcoming song '''
    status_info = ""
    if player.is_playing():
        maybe_current_song: Audio = player.get_playing_audio()
        current_song_name = ""
        if maybe_current_song is None:
            current_song_name = "unknown"
        else:
            current_song_name = maybe_current_song.name
        status_info = f"Currently playing: {current_song_name}."
        maybe_next_audio: Audio = player.get_next_audio()
        if maybe_next_audio is not None:
            status_info +=  f"\nNext song: {maybe_next_audio.name}."
    else:
        status_info = "No audio is playing."
    return status_info

def update_terminal(player: AudioPlayer):
    clean_terminal()
    print(status_information_str(player))
