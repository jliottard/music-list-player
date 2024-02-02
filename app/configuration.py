import os
import toml

TEXT_ENCODING = "utf-8"

def check_required_files_from_configuration_exist() -> bool:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config: dict = toml.load(config_file)
    for profile_associations in config.values():
        for path in profile_associations.values():
            if not os.path.exists(path):
                os.makedirs(path)
                # print(f"Path does not exist: {path}")
                # return False
    return True

def get_audios_directory_path() -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return config["default-profile"]["download-directory-relative-path"]

def get_audio_file_path(audio_name: str) -> str:
    return os.path.join(get_audios_directory_path(), audio_name)

def get_playlist_file_path() -> str:
    with open("configuration.toml", "rt", encoding=TEXT_ENCODING) as config_file:
        config = toml.load(config_file)
    return config["default-profile"]["playlist-file-relative-path"]


