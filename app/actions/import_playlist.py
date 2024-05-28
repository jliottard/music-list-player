from queue import Queue
from threading import Thread
from typing import List, Tuple

from app.config.configuration import Configuration
from app.interface import Interface
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist
from audio_import import audio_loader
from audio_import.audio_metadata import AudioMetadata
from lyrics.lyric_import import prepare_lyrics

def _produce_audio(queue: Queue, configuration: Configuration, meta_query: AudioMetadata, user_interface: Interface):
    """Load the playlist's audios and put them into the queue.
    Assume the user's input is booked
    Free the booked user's input of the <user_interface>
    @param queue Queue: the FIFO's reference to fill of Audio instances
    @param configuration Configuration
    @param meta_query: AudioMetadata, list of keyword the audio metadata must match to be loaded
    @param user_interface: Interface, assume the user's input is booked
    """
    for audio in audio_loader.iterate_over_loading_playlist(
        configuration=configuration,
        meta_query=meta_query,
        user_interface=user_interface
    ):
        prepare_lyrics(audio, configuration, user_interface)
        queue.put(audio)
    queue.put(None)
    if configuration.is_audio_source_selected_on_import():
        user_interface.free_user_input() # allow back main loop to get user's input

def _consume_audio(queue: Queue, player_reference: AudioPlayer):
    """Get audios from the queue and add them to the player until the queue is empty.
    @param queue Queue; a FIFO of Audio instance
    @param player_reference AudioPlayer: the reference to add the queue's audios
    """
    while True:
        audio = queue.get()
        if audio is None:
            break
        player_reference.append_audio_to_player_playlist(audio)

def _load_playlist_in_background(configuration: Configuration, meta_query: AudioMetadata, user_interface: Interface) -> AudioPlayer:
    """Load the playlist's audios in background and early return the player
    @param profile: Profile: the name of a playlist's profile
    @param meta_query: AudioMetadata: optionnal metadata that the audios of the future playlist will match
    @param user_interface: Interface
    @return: AudioPlayer, the reference of the player that the playlist is loaded into.
    """
    loaded_audio_queue = Queue()
    player = AudioPlayer(playlist=Playlist(), volume=AudioPlayer.AUDIO_VOLUME_BASE)
    if configuration.is_audio_source_selected_on_import():
        user_interface.book_user_input() # prevent main loop from getting user's input
    Thread(target=_produce_audio, args=(loaded_audio_queue, configuration, meta_query, user_interface), daemon=True).start()
    Thread(target=_consume_audio, args=(loaded_audio_queue, player), daemon=True).start()
    return player

def import_playlist(args: list, configuration: Configuration, current_player: AudioPlayer, user_interface: Interface) -> AudioPlayer:
    """Get playlist contents from the args' profile and load the player for the audios
    If the args is only containing the import keyword, it loads the whole audio list into a new playlist.
    If the args also contains a tag name, it loads only the tagged audios into the new playlist.
    @param args: List[str]: either contain the import's arguments that must be the name of the profile from
        the configuration file or none argument means the default playlist
    @param current_player AudioPlayer
    @param user_interface: Interface
    @return the player with the loaded playlist,
        or None if the audios cannot be loaded, or if there is not arguments given
    """
    if len(args) < 1:
        return None
    tags = []
    if len(args) > 1:
        # Add arguments as tags to the audios load's query
        tags = args[1:]
    new_player = _load_playlist_in_background(
        configuration=configuration,
        meta_query=AudioMetadata(None, None, None, tags=tags),
        user_interface=user_interface,
    )
    if current_player is not None:
        new_player.set_volume(current_player.get_volume())
        if current_player.is_playing():
            current_player.stop()
    else:
        new_player.set_volume(AudioPlayer.AUDIO_VOLUME_BASE)
    return new_player
