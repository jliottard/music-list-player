from app import configuration

def test_check_required_files_from_configuration_exist():
    assert configuration.check_required_files_from_configuration_exist() is True

def test_get_audios_directory_path_is_string():
    assert isinstance(configuration.get_audios_directory_path(configuration.DEFAULT_PROFILE), str)

def test_get_playlist_file_path_is_string():
    assert isinstance(configuration.get_playlist_file_path(configuration.DEFAULT_PROFILE), str)
