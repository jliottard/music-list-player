import os

from app import configuration
from app.profile import Profile

def is_file_in_cache(absolute_audio_path: str) -> bool:
    return os.path.exists(absolute_audio_path)

def _is_file_loaded(filename_with_extension: str, profile: Profile) -> bool:
    return is_file_in_cache(configuration.get_audio_file_path(filename_with_extension, profile))
