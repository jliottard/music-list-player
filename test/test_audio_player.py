import time

from audio import audio_player, playlist, play_mode, audio, file_extension
from test.environment_for_test import setup_and_teardown_playlist_and_configuration_files

# Constants
FIRST_AUDIO_INDEX = 0
SECOND_AUDIO_INDEX = 1

# Test functions
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
    player = audio_player.AudioPlayer(playlist=config['playlist'], volume=0)
    player.play()
    player.next()
    assert player.get_playing_audio_index() == SECOND_AUDIO_INDEX

def test_set_play_mode_one_pass(setup_and_teardown_playlist_and_configuration_files):
    config: dict = setup_and_teardown_playlist_and_configuration_files
    test_playlist: audio_player.Playlist = config['playlist']
    player = audio_player.AudioPlayer(playlist=test_playlist, volume=0)
    player.set_play_mode(mode=play_mode.PlayMode.ONE_PASS)
    assert player.play_audio_at_index(len(test_playlist.audios) - 1)
    player.next()
    time.sleep(1)   # the player can be slow
    # in one_pass the last audio cannot be skipped since there is not next audio
    assert player.get_playing_audio_index() == len(test_playlist.audios) - 1

def test_set_play_mode_loop(setup_and_teardown_playlist_and_configuration_files):
    config: dict = setup_and_teardown_playlist_and_configuration_files
    test_playlist: audio_player.Playlist = config['playlist']
    player = audio_player.AudioPlayer(playlist=test_playlist, volume=0)
    player.set_play_mode(mode=play_mode.PlayMode.PLAYLIST_LOOP)
    assert player.play_audio_at_index(len(test_playlist.audios) - 1)
    time.sleep(1)   # the player can be slow
    assert player.get_playing_audio_index() == len(test_playlist.audios) - 1
    player.next()
    time.sleep(1)   # the player can be slow
    assert player.get_playing_audio_index() == FIRST_AUDIO_INDEX

def test_play_audio_at_index(setup_and_teardown_playlist_and_configuration_files):
    config: dict = setup_and_teardown_playlist_and_configuration_files
    test_playlist: audio_player.Playlist = config['playlist']
    player = audio_player.AudioPlayer(playlist=test_playlist, volume=0)
    for audio_index in range(len(test_playlist.audios)):
        assert player.play_audio_at_index(audio_index) is True
        time.sleep(1)
        assert player.get_playing_audio_index() == audio_index
    assert player.play_audio_at_index(len(test_playlist.audios)) is False
