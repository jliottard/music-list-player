import math
import os.path
import pytest

from app.config.configuration import Configuration
from app.config.configuration_keyword import ConfigurationKeyword
from audio.audio import Audio
from audio.audio_player import AudioPlayer
from audio.file_extension import FileExtension
from audio.playlist import Playlist
from audio_import import audio_loader
from audio_import.audio_loader import sanitize_filename, UNIX_FORBIDDEN_CHAR, MS_FORBIDDEN_CHAR, ESCAPING_CHAR
from test.environment_for_test import setup_and_teardown_playlist_and_configuration_files
from test.interface_mock import InterfaceMock

def test_sanitize_filename():
    tested_and_expected_filenames = [
        ('there is nothing to remove from', 'there is nothing to remove from'),
        ("".join(UNIX_FORBIDDEN_CHAR), f"{ESCAPING_CHAR}" * len(UNIX_FORBIDDEN_CHAR)),
        ("".join(MS_FORBIDDEN_CHAR), f"{ESCAPING_CHAR}" * len(MS_FORBIDDEN_CHAR))
    ]
    for tested_and_expected_filename in tested_and_expected_filenames:
        tested_filename, expected_filename = tested_and_expected_filename
        assert sanitize_filename(tested_filename) == expected_filename

def test_unload_music(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    playlist: Playlist = test_config['playlist']
    for audio in playlist.audios:
        audio_loader.unload_music(audio=audio, configuration=configuration)
        assert not os.path.isfile(audio.filepath)

def test_load_with_cached_audio(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    playlist: Playlist = test_config['playlist']
    interface_mock: InterfaceMock = InterfaceMock()
    for cached_audio in playlist.audios:
        tested_audio: Audio = audio_loader.load(
            audio_name=cached_audio.name,
            file_extension=FileExtension.MP3,
            configuration=configuration,
            user_interface=interface_mock,
            only_local=False,
            maybe_source=None
        )
        assert tested_audio == cached_audio

def test_load_only_local_audio(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    playlist: Playlist = test_config['playlist']
    interface_mock: InterfaceMock = InterfaceMock()
    not_downloaded_audios = [
        Audio(
            name="this file does not exist",
            filepath="this filepath does not exist either",
            file_extension=FileExtension.MP3
        ),
        Audio(
            name="this second file does not exist too",
            filepath="this filepath does not exist either too",
            file_extension=FileExtension.MP3
        )
    ]
    for not_in_cache_audio in not_downloaded_audios:
        tested_maybe_audio: Audio | None = audio_loader.load(
            audio_name=not_in_cache_audio.name,
            file_extension=FileExtension.MP3,
            configuration=configuration,
            user_interface=interface_mock,
            only_local=True,
            maybe_source=None
        )
        assert tested_maybe_audio is None

def test_load_from_internet(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    playlist: Playlist = test_config['playlist']
    interface_mock: InterfaceMock = InterfaceMock()
    for cached_audio in playlist.audios:
        os.remove(cached_audio.filepath)
    configuration.config[ConfigurationKeyword.USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT] = False
    configuration.config[ConfigurationKeyword.PREPARE_LYRICS_ON_IMPORT] = False
    for cached_audio in playlist.audios:
        tested_audio: Audio = audio_loader.load(
            audio_name=cached_audio.name,
            file_extension=FileExtension.MP3,
            configuration=configuration,
            user_interface=interface_mock,
            only_local=False,
            maybe_source=None
        )
        assert os.path.isfile(tested_audio.filepath)
        assert tested_audio == cached_audio

def test_load_with_source(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    playlist: Playlist = test_config['playlist']
    interface_mock: InterfaceMock = InterfaceMock()
    etude_op_ten_no_four_index = 2
    tested_audio: Audio = audio_loader.load(
        audio_name=playlist.audios[etude_op_ten_no_four_index].name + " test", #change the name to not conflict with the setup
        file_extension=FileExtension.MP3,
        configuration=configuration,
        user_interface=interface_mock,
        only_local=False,
        maybe_source=configuration.profile.audio_metadatas[etude_op_ten_no_four_index].source
    )
    playlist.audios.append(tested_audio)
    player = AudioPlayer(playlist=playlist, volume=0)
    player.play_audio_at_index(2)
    expected_etude_op_ten_no_four_audio_length = 2 * 60 + 20 # 2 minutes 20 second for https://www.youtube.com/watch?v=oHiU-u2ddJ4
    assert int(math.ceil(player.get_playing_audio_duration_in_sec())) == expected_etude_op_ten_no_four_audio_length
    player.play_audio_at_index(len(playlist.audios) - 1)
    expected_etude_op_ten_no_four_audio_length = 2 * 60 + 2 # 2 minutes 2 second for https://www.youtube.com/watch?v=oy0IgI_qewg
    assert int(math.ceil(player.get_playing_audio_duration_in_sec())) == expected_etude_op_ten_no_four_audio_length
