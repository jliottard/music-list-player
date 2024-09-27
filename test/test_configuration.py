import pytest

from test.conftest import setup_and_teardown_playlist_and_configuration_files

from app.config.configuration import Configuration

def test_search_missing_but_required_files_from_configuration_exist(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    # all file must be set up for this unit test, so it is expected to have none missing files
    assert len(configuration.search_missing_but_required_files_from_configuration_exist()) == 0

def test_get_audios_directory_path_is_string(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.get_audios_directory_path(), str)

def test_get_playlist_file_path_is_string(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.get_playlist_file_path(), str)

def test_is_audio_cache_persistant_is_boolean(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.is_audio_cache_persistant(), bool)

def test_is_music_lyrics_searched_on_import_is_boolean(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.is_music_lyrics_searched_on_import(), bool)

def test_is_audio_source_selection_on_import_is_boolean(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.is_audio_source_selected_on_import(), bool)

def test_is_default_profile_import_on_startup_is_boolean(setup_and_teardown_playlist_and_configuration_files):
    configuration: Configuration = setup_and_teardown_playlist_and_configuration_files['configuration']
    assert isinstance(configuration.is_default_profile_imported_on_startup(), bool)
