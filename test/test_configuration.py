import pytest

from app.config.configuration import Configuration, CONFIGURATION_FILE_PATH, TEXT_ENCODING
from app.config.profile import Profile

TEST_PROFILE_CONFIGURATION = "\n".join(
    [
        '',
        '[test]',
        '"download-directory-relative-path" = "audios_cache"',
        '"playlist-file-relative-path" = "playlists/test_playlist.txt"',
        '"persistant-audio-cache" = false',
        '"music-lyrics-search-on-import" = true',
        '"audio-source-selection-on-import" = false'
        ''
    ]
)

@pytest.fixture
def setup_and_teardown_test_configuration():
    # Setup
    configuration_path = CONFIGURATION_FILE_PATH
    configuration_backup = ''
    with open(configuration_path, "rt", encoding=TEXT_ENCODING) as config_file:
        configuration_backup = config_file.read()
    with open(configuration_path, "at", encoding=TEXT_ENCODING) as config_file:
        config_file.write(TEST_PROFILE_CONFIGURATION)
    yield Configuration(Profile('test'), configuration_path)
    # Teardown
    with open(configuration_path, "wt", encoding=TEXT_ENCODING) as config_file:
        config_file.write(configuration_backup)

def test_check_required_files_from_configuration_exist(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert configuration.check_required_files_from_configuration_exist() is True

def test_get_audios_directory_path_is_string(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.get_audios_directory_path(), str)

def test_get_playlist_file_path_is_string(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.get_playlist_file_path(), str)

def test_is_audio_cache_persistant_is_boolean(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.is_audio_cache_persistant(), bool)

def test_is_music_lyrics_searched_on_import_is_boolean(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.is_music_lyrics_searched_on_import(), bool)

def test_is_audio_source_selection_on_import_is_boolean(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.is_audio_source_selected_on_import(), bool)

def test_is_default_profile_import_on_startup_is_boolean(setup_and_teardown_test_configuration):
    configuration = setup_and_teardown_test_configuration
    assert isinstance(configuration.is_default_profile_imported_on_startup(), bool)
