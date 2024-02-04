from typing import Tuple

from app import configuration
from audio.audio_player import AudioPlayer
from audio.file_import import audio_loader
from audio.playlist import Playlist

def import_defaut_playlist(player: AudioPlayer) -> Tuple[Playlist, AudioPlayer]:
    """ Check playlist audio files are available locally and generate a new playlist and player"""
    if player is not None:
        player.stop()
    playlist_path = configuration.get_playlist_file_path()
    playlist = Playlist()
    playlist.audios = audio_loader.import_playlist_audios(playlist_file_absolute_path=playlist_path)
    player = AudioPlayer(playlist)
    return playlist, player
