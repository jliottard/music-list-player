import os
from typing import List
import toml

from app.config.configuration_keyword import ConfigurationKeyword, GLOBAL_APP_SETTINGS_NAME
from app.config.profile import Profile

# Constants
TEXT_ENCODING = "utf-8"
CONFIGURATION_FILE_PATH = "configuration.toml"

# Functions
def operating_system_proof_path(path: str) -> str:
    """Return a absolute path that is separated according to the runner machine's operating system"""
    return os.path.abspath(os.path.expanduser(path))

def is_a_directory_path_keyword(string: str) -> bool:
    return "path" in string and "directory" in string


# Class
class Configuration():
    """TODO: class desc"""

    def __init__(self, profile: Profile, configuration_filepath: str = CONFIGURATION_FILE_PATH):
        self.config: dict = self.load_configuration(configuration_filepath)
        self.profile: Profile = profile

    def load_configuration(self, configuration_filepath: str) -> dict:
        '''Load the TOML configuration file into a Python dict
        @param configuration_filepath: str
        @return the Dict representation of that configuration
        '''
        with open(configuration_filepath, "rt", encoding=TEXT_ENCODING) as config_file:
            return toml.load(config_file)

    def check_required_files_from_configuration_exist(self) -> bool:
        for settings in self.config.values():
            for setting_name, setting_value in settings.items():
                if isinstance(setting_name, str) and is_a_directory_path_keyword(setting_name):
                    os_proof_path = operating_system_proof_path(setting_value)
                    if not os.path.exists(os_proof_path):
                        os.mkdir(os_proof_path)
        return True

    def get_audios_directory_path(self) -> str:
        return operating_system_proof_path(self.config[self.profile.name][ConfigurationKeyword.CACHE_DIRECTORY_PATH.value])

    def get_audio_file_path(self, audio_name: str) -> str:
        return operating_system_proof_path(os.path.join(self.get_audios_directory_path(), audio_name))

    def get_playlist_file_path(self) -> str:
        """Return the absolute path to the playlist text file"""
        return operating_system_proof_path(self.config[self.profile.name][ConfigurationKeyword.PLAYLIST_PATH.value])

    def is_audio_cache_persistant(self) -> bool:
        return self.config[self.profile.name][ConfigurationKeyword.KEEP_CACHE_POLICY.value]

    def is_music_lyrics_searched_on_import(self) -> bool:
        return self.config[self.profile.name][ConfigurationKeyword.PREPARE_LYRICS_ON_IMPORT.value]

    def is_audio_source_selected_on_import(self) -> bool:
        return self.config[self.profile.name][ConfigurationKeyword.USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT.value]

    def is_default_profile_imported_on_startup(self) -> bool:
        return self.config[GLOBAL_APP_SETTINGS_NAME][ConfigurationKeyword.AUTO_IMPORT_DEFAUT_PLAYLIST_ON_STARTUP.value]

    def get_profiles(self) -> List[str]:
        return self.config.keys()
