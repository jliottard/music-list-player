import os
import toml

TEXT_ENCODING = "utf-8"
CONFIGURATION_FILE_PATH = "configuration.toml"
CONFIGURATION_PLAYLIST_PATH_KEYWORD = "playlist-file-relative-path"
CONFIGURATION_CACHE_DIRECTORY_PATH_KEYWORD = "download-directory-relative-path"
DEFAULT_PROFILE = "default"

def operating_system_proof_path(path: str) -> str:
    """ Return a absolute path that is separated according to the runner machine's operating system """
    return os.path.abspath(os.path.expanduser(path))

def _get_profile_suffix(name: str) -> str:
    return name + "-profile"

def check_required_files_from_configuration_exist() -> bool:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config: dict = toml.load(config_file)
    for profile_associations in config.values():
        for path in profile_associations.values():
            os_proof_path = operating_system_proof_path(path)
            if not os.path.exists(os_proof_path):
                os.makedirs(os_proof_path)
                # print(f"Path does not exist: {path}")
                # return False
    return True

def get_audios_directory_path(profile_name: str) -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config[_get_profile_suffix(profile_name)][CONFIGURATION_CACHE_DIRECTORY_PATH_KEYWORD])

def get_audio_file_path(audio_name: str, profile_name: str) -> str:
    return operating_system_proof_path(os.path.join(get_audios_directory_path(profile_name), audio_name))

def get_playlist_file_path(profile_name: str) -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config[_get_profile_suffix(profile_name)][CONFIGURATION_PLAYLIST_PATH_KEYWORD])
