import os
import shutil
import platform
import pytest

from app.file_management import remove_file_extension_part
from app.config.configuration import Configuration, TEXT_ENCODING
from app.path import operating_system_proof_path
from app.config.profile import Profile
from audio.audio import Audio
from audio.file_extension import FileExtension
from audio_import import youtube_metadata_parser, audio_loader, youtube_download, plain_text_parse
from audio_import.youtube_video_metadata import YouTubeVideoMetadata
from audio.playlist import Playlist
from test.interface_mock import InterfaceMock

MAX_CACHE_INIT_ATTEMPTS = 5

# Path constants
TEST_WORK_DIRECTORY_RELATIVE_PATH = 'test/test_workspace'
TEST_CACHE_DIRECTORY_RELATIVE_PATH = 'test/test_cache'
if platform.system() == "Linux":
    TEST_WORK_DIRECTORY_RELATIVE_PATH = operating_system_proof_path(TEST_WORK_DIRECTORY_RELATIVE_PATH)
    TEST_CACHE_DIRECTORY_RELATIVE_PATH = operating_system_proof_path(TEST_CACHE_DIRECTORY_RELATIVE_PATH)

TEST_PLAYLIST_RELATIVE_PATH = '/'.join(
    [
        TEST_WORK_DIRECTORY_RELATIVE_PATH,
        'playlist_for_test.txt'
    ]
)
TEST_CACHED_AUDIO_DIRECTORY_PATH = '/'.join(
    [
        TEST_WORK_DIRECTORY_RELATIVE_PATH,
        'audio_cache_for_test'
    ]
)
TEST_PROFILE_CONFIGURATION_RELATIVE_PATH = '/'.join(
    [
        TEST_WORK_DIRECTORY_RELATIVE_PATH,
        'configuration_for_test.toml'
    ]
)

TEST_PROFILE_NAME = 'test'

TEST_PROFILE_CONFIGURATION_CONTENTS = "\n".join(
    [
        '[global-settings]',
        '"default-profile-import-on-startup" = false',
        f"\"default-profile-name\" = \"{TEST_PROFILE_NAME}\"",
        f"[{TEST_PROFILE_NAME}]",
        f"\"download-directory-relative-path\" = \"{TEST_CACHED_AUDIO_DIRECTORY_PATH}\"",
        f"\"playlist-file-relative-path\" = \"{TEST_PLAYLIST_RELATIVE_PATH}\"",
        '"persistant-audio-cache" = false',
        '"music-lyrics-search-on-import" = false',
        '"audio-source-selection-on-import" = false',
        ' '
    ]
)

TEST_PLAYLIST_FILE_CONTENTS = f"\n".join(
    [
        'nocturne op 55 no 1 by frédéric chopin #chopin',
        'nocturne op 9 no 2 by frédéric chopin #chopin',
        'etude op 10 no 4 by frédéric chopin #chopin (https://www.youtube.com/watch?v=oy0IgI_qewg)',
        'hungarian dance no 5 by johannes brahms'
    ]
)

TEST_CONFIGURATION: dict = None
AUDIO_FILE_EXTENSION = FileExtension.MP3



def init_cache_test():
    """Download only once the audios then copy them at each test's start"""
    global TEST_CACHE_DIRECTORY_RELATIVE_PATH
    global TEST_PLAYLIST_FILE_CONTENTS
    global AUDIO_FILE_EXTENSION
    os.makedirs(TEST_CACHE_DIRECTORY_RELATIVE_PATH)
    try:
        for line in TEST_PLAYLIST_FILE_CONTENTS.split("\n"):
            audio_metadata = plain_text_parse._playlist_line_to_audio_metadata(line)
            audio_name = audio_loader.sanitize_filename(audio_metadata.name)
            youtube_videos_metadatas = youtube_metadata_parser.search_videos_on_youtube(audio_name)
            maybe_chosen_youtube_video: YouTubeVideoMetadata | None = audio_loader._get_first_youtube_result(youtube_videos_metadatas)
            assert maybe_chosen_youtube_video is not None
            chosen_youtube_video: YouTubeVideoMetadata = maybe_chosen_youtube_video
            audio_download_absolute_path = youtube_download.download_audio_from_youtube(
                youtube_url=chosen_youtube_video.url,
                output_directory_relative_path=TEST_CACHE_DIRECTORY_RELATIVE_PATH
            )
            renamed_filepath = audio_loader._rename_filename(
                source_filepath=audio_download_absolute_path,
                new_filename_with_extension=audio_name + AUDIO_FILE_EXTENSION.value
            )
    except Exception as e:
        shutil.rmtree(TEST_CACHE_DIRECTORY_RELATIVE_PATH, ignore_errors=True)
        raise e
    return True

# Global setup for the entire testsuite
@pytest.hookimpl()
def pytest_sessionstart(session):
    print("\nTest session has begun.")
    init_remaining_attempts = MAX_CACHE_INIT_ATTEMPTS
    init_is_successful = False
    while not init_is_successful and init_remaining_attempts > 0:
        try:
            init_is_successful = init_cache_test()
        except:
            init_remaining_attempts -= 1
            print(f"Cache initialization for test failed. Remaining attempts: {init_remaining_attempts}/{MAX_CACHE_INIT_ATTEMPTS}")
    print("\nTest session is set and ready.")

# Global teardown for the entire testsuite
@pytest.hookimpl()
def pytest_sessionfinish(session):
    print("\nTest session has finished!")
    # Teardown
    shutil.rmtree(TEST_CACHE_DIRECTORY_RELATIVE_PATH)

# Local setup and local_teardown for each test
def local_setup():
    print("\nLocal setup is being set.")
    global TEST_CONFIGURATION
    # Setup
    if os.path.isdir(TEST_WORK_DIRECTORY_RELATIVE_PATH):
        shutil.rmtree(TEST_WORK_DIRECTORY_RELATIVE_PATH)
    
    os.makedirs(TEST_WORK_DIRECTORY_RELATIVE_PATH, exist_ok=True)
    with open(TEST_PROFILE_CONFIGURATION_RELATIVE_PATH, "wt", encoding=TEXT_ENCODING) as config_file:
        config_file.write(TEST_PROFILE_CONFIGURATION_CONTENTS)
    with open(TEST_PLAYLIST_RELATIVE_PATH, "wt", encoding=TEXT_ENCODING) as playlist_file:
        playlist_file.write(TEST_PLAYLIST_FILE_CONTENTS)

    profile = Profile(TEST_PROFILE_NAME)
    configuration = Configuration(profile, TEST_PROFILE_CONFIGURATION_RELATIVE_PATH)
    mock_interface = InterfaceMock()
    configuration.fill_profile_with_metadata(mock_interface)
    playlist = Playlist()

    os.makedirs(TEST_CACHED_AUDIO_DIRECTORY_PATH, exist_ok=True)
    for cache_file in os.listdir(TEST_CACHE_DIRECTORY_RELATIVE_PATH):
        cache_filepath = os.path.join(TEST_CACHE_DIRECTORY_RELATIVE_PATH, cache_file)
        workspace_cache_filepath = os.path.join(TEST_CACHED_AUDIO_DIRECTORY_PATH, cache_file)
        shutil.copyfile(cache_filepath, workspace_cache_filepath)
        playlist.audios.append(
            Audio(
                name_without_extension=remove_file_extension_part(cache_file),
                filepath=workspace_cache_filepath,
                file_extension=AUDIO_FILE_EXTENSION
            )
        )
    TEST_CONFIGURATION = {
        'configuration': configuration,
        'configuration_path': TEST_PROFILE_CONFIGURATION_RELATIVE_PATH,
        'playlist_path': TEST_PLAYLIST_RELATIVE_PATH,
        'playlist': playlist
    }
    print("\nLocal setup is set.")

def local_teardown():
    print("\nLocal teardown is being executed.")
    shutil.rmtree(TEST_WORK_DIRECTORY_RELATIVE_PATH)

@pytest.fixture(autouse=True)
def run_around_tests():
    global TEST_CONFIGURATION
    local_setup()
    yield TEST_CONFIGURATION
    local_teardown()

@pytest.fixture
def setup_and_teardown_playlist_and_configuration_files():
    global TEST_CONFIGURATION
    yield TEST_CONFIGURATION
