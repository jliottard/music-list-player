from app.interface import Interface
from audio.audio_player import AudioPlayer

def shuffle_playlist(player: AudioPlayer, user_interface: Interface):
    """Rearrange the order of the player's playlist
    @param player: AudioPlayer
    @param user_interface: Interface
    """
    current_audio = player.get_playing_audio()
    player.stop()
    user_interface.request_output_to_user("Info: Shuffling the playlist.")
    player.shuffle()
    index = player.get_index_of_audio(current_audio)
    player.play_audio_at_index(index)
