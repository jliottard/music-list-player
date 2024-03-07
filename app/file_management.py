import os

from app import configuration

def _is_file_in_cache(absolute_audio_path: str) -> bool:
    return os.path.exists(absolute_audio_path)

def _is_file_loaded(filename_with_extension: str, profile: str) -> bool:
    return _is_file_in_cache(configuration.get_audio_file_path(filename_with_extension, profile))
