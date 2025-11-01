from app.interface import Interface
from app.message_priority import MessagePriority
from audio.audio import Audio
from audio.audio_player import AudioPlayer

def shuffle_playlist(player: AudioPlayer, user_interface: Interface):
    """Rearrange the order of the player's playlist, pause and resume the played audio
    @param player: AudioPlayer
    @param user_interface: Interface
    """
    maybe_current_audio: Audio | None = player.get_playing_audio()
    maybe_time_progression_in_sec: float | None = player.get_audio_progress_time_in_sec()
    player.stop()
    user_interface.request_output_to_user("Info: Shuffling the playlist.", MessagePriority.INFO)
    player.shuffle()
    if maybe_current_audio is not None:
        player.play_audio_at_index(player.get_index_of_audio(maybe_current_audio))
    if maybe_time_progression_in_sec is not None:
        player.set_current_audio_time(int(maybe_time_progression_in_sec))
