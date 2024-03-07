import os
import pytest

from app import configuration

TEST_PROFILE_CONFIGURATION = "\n".join(
        [
            '',
            '[test-profile]',
            '"download-directory-relative-path" = "audios_cache"',
            '"playlist-file-relative-path" = "playlists/test_playlist.txt"',
            '"persistant-audio-cache" = false',
            '"music-lyrics-search-on-import" = true',
            ''
        ]
    )

@pytest.fixture
def setup_and_teardown_test_configuration():
    # Setup
    configuration_path = configuration.CONFIGURATION_FILE_PATH
    configuration_backup = ''
    with open(configuration_path, "rt", encoding=configuration.TEXT_ENCODING) as config_file:
        configuration_backup = config_file.read()
    with open(configuration_path, "at", encoding=configuration.TEXT_ENCODING) as config_file:
        config_file.write(TEST_PROFILE_CONFIGURATION)
    yield 'test'
    # Teardown
    with open(configuration_path, "wt", encoding=configuration.TEXT_ENCODING) as config_file:
        config_file.write(configuration_backup)

def test_check_required_files_from_configuration_exist():
    assert configuration.check_required_files_from_configuration_exist() is True

def test_get_audios_directory_path_is_string(setup_and_teardown_test_configuration):
    assert isinstance(configuration.get_audios_directory_path(setup_and_teardown_test_configuration), str)

def test_get_playlist_file_path_is_string(setup_and_teardown_test_configuration):
    assert isinstance(configuration.get_playlist_file_path(setup_and_teardown_test_configuration), str)

def test_is_audio_cache_persistant_is_boolean(setup_and_teardown_test_configuration):
    assert isinstance(configuration.is_audio_cache_persistant(setup_and_teardown_test_configuration), bool)

def test_is_music_lyrics_searched_on_import_is_boolean(setup_and_teardown_test_configuration):
    assert isinstance(configuration.is_music_lyrics_searched_on_import(setup_and_teardown_test_configuration), bool)
