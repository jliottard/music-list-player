from app.interface import Interface
from audio.audio import Audio
from audio.audio_player import AudioPlayer

def skip_music(player: AudioPlayer, user_interface: Interface) -> None:
    """Make the player play the following the music
    @param player: AudioPlayer
    @param user_interface: Interface
    """
    maybe_next_audio: Audio = player.get_next_audio()
    if maybe_next_audio is None:
        user_interface.request_output_to_user("Cannot skip, end of playlist reached as one pass mode.")
    else:
        player.next()
        user_interface.request_output_to_user(f"Skipping to \"{maybe_next_audio.name}\".")
