import os
import toml

TEXT_ENCODING = "utf-8"

def operating_system_proof_path(path: str) -> str:
    """ Return a absolute path that is separated according to the runner machine's operating system """
    return os.path.abspath(os.path.expanduser(path))

def check_required_files_from_configuration_exist() -> bool:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config: dict = toml.load(config_file)
    for profile_associations in config.values():
        for path in profile_associations.values():
            os_proof_path = operating_system_proof_path(path)
            if not os.path.exists(os_proof_path):
                os.makedirs(os_proof_path)
                # print(f"Path does not exist: {path}")
                # return False
    return True

def get_audios_directory_path() -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config["default-profile"]["download-directory-relative-path"])

def get_audio_file_path(audio_name: str) -> str:
    return operating_system_proof_path(os.path.join(get_audios_directory_path(), audio_name))

def get_playlist_file_path() -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return operating_system_proof_path(config["default-profile"]["playlist-file-relative-path"])


