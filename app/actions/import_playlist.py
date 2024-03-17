from queue import Queue
from threading import Thread
from typing import Tuple, List

from app import configuration
from audio.audio_player import AudioPlayer
from audio_import import audio_loader
from audio.playlist import Playlist
from lyrics.lyric_import import prepare_lyrics

def _produce_audio(queue: Queue, playlist_path: str, profile: str):
    '''Load the playlist's audios and put them into the queue
    @param queue Queue: the FIFO's reference to fill of Audio instances
    @param playlist_path str: absolute path to the playlist file
    @param profile str: playlist's profile from the configuration file
    '''
    for audio in audio_loader.iterate_over_loading_playlist(
        playlist_file_absolute_path=playlist_path,
        playlist_profile=profile
    ):
        prepare_lyrics(audio, profile)
        queue.put(audio)
    queue.put(None)

def _consume_audio(queue: Queue, player_reference: AudioPlayer):
    '''Get audios from the queue and add them to the player until the queue is empty.
    @param queue Queue; a FIFO of Audio instance
    @param player_reference AudioPlayer: the reference to add the queue's audios
    '''
    while True:
        audio = queue.get()
        if audio is None:
            break
        player_reference.append_audio_to_playlist(audio)

def _load_playlist_in_background(playlist_path: str, profile: str) -> AudioPlayer:
    ''' Load the playlist's audios in background and early return the player
    @param playlist_path: str: the absolute path to the text file containing the audios' name
    @param profile: str: the name of a playlist's profile
    @return: AudioPlayer, the reference of the player that the playlist is loaded into.
    '''
    loaded_audio_queue = Queue()
    player = AudioPlayer(playlist=Playlist(), volume=AudioPlayer.AUDIO_VOLUME_BASE)
    Thread(target=_produce_audio, args=(loaded_audio_queue, playlist_path, profile), daemon=True).start()
    Thread(target=_consume_audio, args=(loaded_audio_queue, player), daemon=True).start()
    return player

def import_playlist(args: List[str], current_player: AudioPlayer) -> Tuple[AudioPlayer, str]:
    ''' Get playlist contents from the args' profile and load the player for the audios
    @param: args: List[str]: either contain the import's arguments that must be the name of the profile from the configuration file or none argument means the default playlist
    @return the player with the loaded playlist and the profile, or None if the audios cannot be loaded
    '''
    if len(args) < 1:
        return None
    profile = None
    if len(args) == 1:
        profile = configuration.DEFAULT_PLAYLIST_PROFILE_NAME
    else:
        profile = str(args[1])
    playlist_path = configuration.get_playlist_file_path(profile)
    new_player = _load_playlist_in_background(
        playlist_path=playlist_path,
        profile=profile
    )
    if current_player is not None:
        new_player.set_volume(current_player.get_volume())
        if current_player.is_playing():
            current_player.stop()
    else:
        new_player.set_volume(AudioPlayer.AUDIO_VOLUME_BASE)
    return new_player, profile
