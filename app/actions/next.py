from audio.audio_player import AudioPlayer
from audio.play_mode import PlayMode

def skip_music(player: AudioPlayer) -> None:
    """ Make the player play the following the music """
    maybe_playing_audio_index = player.get_playing_audio_index()
    if maybe_playing_audio_index is None:
        next_audio_name = ".."
    else:
        next_audio_index = (maybe_playing_audio_index + 1) % len(player.playlist.audios)
        next_audio_name = player.playlist.names()[next_audio_index]
    is_playing_audio_last = player.get_playing_audio_index() == len(player.playlist.audios) - 1
    if is_playing_audio_last:
        match player.get_play_mode():
            case PlayMode.PLAYLIST_LOOP:
                player.play_audio_at_index(0)
            case PlayMode.ONE_PASS:
                print("Cannot skip, end of playlist reached as one pass mode.")
                return
            case _:
                pass
    else:
        player.next()
    print(f"Skipping to \"{next_audio_name}\".")
