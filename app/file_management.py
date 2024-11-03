import os

from app.config.configuration import Configuration

def is_file_in_cache(absolute_audio_path: str) -> bool:
    '''True if file exists, False otherwise'''
    return os.path.exists(absolute_audio_path)

def _is_file_loaded(filename_with_extension: str, configuration: Configuration) -> bool:
    '''True if file exists in the configuration and in the file system'''
    return is_file_in_cache(configuration.get_audio_file_path(filename_with_extension))

def remove_file_extension_part(filepath: str) -> str:
    '''Extract the first part of the filepath, splitting the .extension part'''
    filepath_base, _video_extension = os.path.splitext(filepath)
    return filepath_base