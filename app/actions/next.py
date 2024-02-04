from audio.audio import Audio
from audio.audio_player import AudioPlayer

def skip_music(player: AudioPlayer) -> None:
    """ Make the player play the following the music """
    maybe_next_audio: Audio = player.get_next_audio()
    if maybe_next_audio is None:
        print("Cannot skip, end of playlist reached as one pass mode.")
    else:
        player.next()
        print(f"Skipping to \"{maybe_next_audio.name}\".")
