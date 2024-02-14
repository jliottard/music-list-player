from typing import Tuple, List

from app import configuration
from app.command import Command
from audio.audio_player import AudioPlayer
from audio.file_import import audio_loader
from audio.playlist import Playlist

def import_defaut_playlist(player: AudioPlayer) -> Tuple[AudioPlayer, str]:
    """ Check playlist audio files are available locally and generate a new playlist and player"""
    return import_playlist([Command.IMPORT.value, configuration.DEFAULT_PROFILE], player)

def import_playlist(args: List[str], player: AudioPlayer) -> Tuple[AudioPlayer, str]:
    ''' Get playlist contents from the args' profile and load the player for the audios
    @param: args: List[str]: contains in the second argument that must be the name of the profile from the configuration file
    @return the player with the loaded playlist, or None if the audios cannot be loaded
    '''
    if len(args) < 2:
        return None
    profile = str(args[1])
    playlist_path = configuration.get_playlist_file_path(profile)
    playlist = Playlist()
    playlist.audios = audio_loader.import_playlist_audios(
        playlist_file_absolute_path=playlist_path,
        playlist_profile=profile
    )
    if player.is_playing():
        played_volume = player.get_volume()
        if player is not None:
            player.stop()
        player = AudioPlayer(playlist, played_volume)
    else:
        player = AudioPlayer(playlist, AudioPlayer.AUDIO_VOLUME_BASE)
    return player, profile
