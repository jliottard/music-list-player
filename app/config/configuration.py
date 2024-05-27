import os
from typing import List
import toml

from app.config.configuration_keyword import ConfigurationKeyword, GLOBAL_APP_SETTINGS_NAME
from app.config.profile import Profile
from app.interface import Interface

from audio_import.audio_metadata import AudioMetadata
from audio_import.plain_text_parse import parse_plain_text_playlist_file

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
    """Class representing the app configuration's state from the TOML configuration file and its profile"""

    def __init__(self, profile: Profile, configuration_filepath: str = CONFIGURATION_FILE_PATH):
        self.config: dict = self.load_configuration(configuration_filepath)
        if profile is None:
            self.profile = Profile(self.get_default_profile_name())
        else:
            self.profile: Profile = profile

    def load_configuration(self, configuration_filepath: str) -> dict:
        '''Load the TOML configuration file into a Python dict
        @param configuration_filepath: str
        @return the Dict representation of that configuration
        '''
        with open(configuration_filepath, "rt", encoding=TEXT_ENCODING) as config_file:
            return toml.load(config_file)

    def fill_profile_with_metadata(self, user_interface: Interface):
        """File the metadata fields of profile
        @param configuration: Configuration
        @param user_interface: Interface
        @return Profile: the same profile
        """
        self.profile.audio_metadatas: List[AudioMetadata] = parse_plain_text_playlist_file(
            playlist_file_absolute_path=self.get_playlist_file_path(),
            user_interface=user_interface,
            text_encoding=TEXT_ENCODING
        )

    def search_missing_but_required_files_from_configuration_exist(self) -> List[str]:
        '''Search for the filepath defined in the profile that are not existing on the machine
        @return List[str], the list of missing filepath
        '''
        missing_filepaths = []
        for settings in self.config.values():
            for setting_name, setting_value in settings.items():
                if isinstance(setting_name, str) and is_a_directory_path_keyword(setting_name):
                    os_proof_path = operating_system_proof_path(setting_value)
                    if not os.path.exists(os_proof_path):
                        missing_filepaths.append(os_proof_path)
        return missing_filepaths

    def check_default_profile_is_defined_in_configuration(self) -> bool:
        '''Return True if the default profile is defined, False otherwise'''
        return self.get_default_profile_name() in self.get_profiles()

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

    def get_default_profile_name(self) -> bool:
        return self.config[GLOBAL_APP_SETTINGS_NAME][ConfigurationKeyword.DEFAULT_PLAYLIST_NAME.value]

    def get_profiles(self) -> List[str]:
        return self.config.keys()
