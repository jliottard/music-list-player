from audio import audio_player, playlist, audio, file_extension
from test.environment_for_test import setup_and_teardown_playlist_and_configuration_files

def test_audio_player_audios_order():
    audios = []
    for i in range(100):
        audio_name = "audio" + str(i)
        audio_path = "path/to/" + audio_name
        audios.append(
            audio.Audio(audio_name, audio_path, file_extension.FileExtension.MP3)
        )
    tested_playlist = playlist.Playlist()
    tested_playlist.audios = audios
    tested_audio_player = audio_player.AudioPlayer(tested_playlist, audio_player.AudioPlayer.AUDIO_VOLUME_BASE)
    for i, tested_audio in enumerate(audios):
        assert tested_audio_player.get_index_of_audio(tested_audio) == i

def test_get_playing_audio_index_in_non_playing_player():
    tested_audio_player = audio_player.AudioPlayer(playlist.Playlist(), audio_player.AudioPlayer.AUDIO_VOLUME_BASE)
    assert tested_audio_player.get_playing_audio_index() is None

def test_play_audio_at_index_in_empty_player_playlist():
    tested_audio_player = audio_player.AudioPlayer(playlist.Playlist(), audio_player.AudioPlayer.AUDIO_VOLUME_BASE)
    assert tested_audio_player.play_audio_at_index(0) is False

def test_audio_player_next(setup_and_teardown_playlist_and_configuration_files):
    config: dict = setup_and_teardown_playlist_and_configuration_files
    
    # TODO test something interesting / relevant