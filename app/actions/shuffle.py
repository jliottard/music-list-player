from audio.audio_player import AudioPlayer

def shuffle_playlist(player: AudioPlayer):
    """ Rearrange the order of the player's playlist """
    current_audio = player.get_playing_audio()
    player.stop()
    print("Shuffling the playlist.")
    player.shuffle()
    index = player.get_index_of_audio(current_audio)
    player.play_audio_at_index(index)
