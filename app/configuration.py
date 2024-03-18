import os
import toml

# Constants
TEXT_ENCODING = "utf-8"
CONFIGURATION_FILE_PATH = "configuration.toml"
CONFIGURATION_PLAYLIST_PATH_KEYWORD = "playlist-file-relative-path"
CONFIGURATION_CACHE_DIRECTORY_PATH_KEYWORD = "download-directory-relative-path"
CONFIGURATION_KEEP_CACHE_POLICY_KEYWORD = "persistant-audio-cache"
CONFIGURATION_PREPARE_LYRICS_ON_IMPORT_KEYWORD = "music-lyrics-search-on-import"
DEFAULT_PLAYLIST_PROFILE_NAME = "default"
CONFIGURATION_USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT_KEYWORD = "audio-source-selection-on-import"

# Functions
def operating_system_proof_path(path: str) -> str:
    """Return a absolute path that is separated according to the runner machine's operating system"""
    return os.path.abspath(os.path.expanduser(path))

def _get_profile_suffix(name: str) -> str:
    return name + "-profile"

def is_a_directory_path_keyword(string: str) -> bool:
    return "path" in string and "directory" in string

def check_required_files_from_configuration_exist() -> bool:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config: dict = toml.load(config_file)
    for settings in config.values():
        for setting_name, setting_value in settings.items():
            if isinstance(setting_name, str) and is_a_directory_path_keyword(setting_name):
                os_proof_path = operating_system_proof_path(setting_value)
                if not os.path.exists(os_proof_path):
                    os.mkdir(os_proof_path)
    return True

def get_audios_directory_path(profile_name: str) -> str:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config[_get_profile_suffix(profile_name)][CONFIGURATION_CACHE_DIRECTORY_PATH_KEYWORD])

def get_audio_file_path(audio_name: str, profile_name: str) -> str:
    return operating_system_proof_path(os.path.join(get_audios_directory_path(profile_name), audio_name))

def get_playlist_file_path(profile_name: str) -> str:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config[_get_profile_suffix(profile_name)][CONFIGURATION_PLAYLIST_PATH_KEYWORD])

def is_audio_cache_persistant(profile_name: str) -> bool:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return config[_get_profile_suffix(profile_name)][CONFIGURATION_KEEP_CACHE_POLICY_KEYWORD]

def is_music_lyrics_searched_on_import(profile_name: str) -> bool:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return config[_get_profile_suffix(profile_name)][CONFIGURATION_PREPARE_LYRICS_ON_IMPORT_KEYWORD]

def is_audio_source_selected_on_import(profile_name: str) -> bool:
    with open(CONFIGURATION_FILE_PATH, "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return config[_get_profile_suffix(profile_name)][CONFIGURATION_USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT_KEYWORD]
