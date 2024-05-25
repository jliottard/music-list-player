import os

from app.config.configuration import Configuration

def is_file_in_cache(absolute_audio_path: str) -> bool:
    return os.path.exists(absolute_audio_path)

def _is_file_loaded(filename_with_extension: str, configuration: Configuration) -> bool:
    return is_file_in_cache(configuration.get_audio_file_path(filename_with_extension))
