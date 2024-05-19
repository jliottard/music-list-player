import os
import shutil
import pytest

from app.actions.change_profile import _fill_profile_with_metadata
from app.config.configuration import Configuration, TEXT_ENCODING
from app.config.profile import Profile
from audio.audio import Audio
from audio_import import youtube_metadata_parser, audio_loader, youtube_download, plain_text_parse
from audio.playlist import Playlist
from test.interface_mock import InterfaceMock

TEST_WORK_DIRECTORY_RELATIVE_PATH = "test/test_workspace"

TEST_PLAYLIST_RELATIVE_PATH = os.path.join(
    TEST_WORK_DIRECTORY_RELATIVE_PATH,
    "playlist_for_test.txt"
)
TEST_PLAYLIST_FILE_CONTENTS = "\n".join(
    [
        'nocturne op. 55 no 1 by frédéric chopin #chopin',
        'nocturne op.9 no 2 by frédéric chopin #chopin',
        'etude op 10 no 4 by frédéric chopin #chopin (https://www.youtube.com/watch?v=oHiU-u2ddJ4) '
        'hungarian dance no 5 by johannes brahms'
    ]
)

TEST_PROFILE_NAME = 'test'
TEST_CACHED_AUDIO_DIRECTORY_PATH = os.path.join(
    TEST_WORK_DIRECTORY_RELATIVE_PATH,
    "audio_cache_for_test"
)
TEST_PROFILE_CONFIGURATION_RELATIVE_PATH = os.path.join(
    TEST_WORK_DIRECTORY_RELATIVE_PATH,
    "configuration_for_test.toml"
)
TEST_PROFILE_CONFIGURATION_CONTENTS = "\n".join(
    [
        '[global-settings]',
        '"default-profile-import-on-startup" = false',
        f"[{TEST_PROFILE_NAME}]",
        f"\"download-directory-relative-path\" = \"{TEST_CACHED_AUDIO_DIRECTORY_PATH}\"",
        f"\"playlist-file-relative-path\" = \"{TEST_PLAYLIST_RELATIVE_PATH}\"",
        '"persistant-audio-cache" = false',
        '"music-lyrics-search-on-import" = false',
        '"audio-source-selection-on-import" = false',
        ''
    ]
)

@pytest.fixture
def setup_and_teardown_playlist_and_configuration_files():
    # Setup
    os.makedirs(TEST_WORK_DIRECTORY_RELATIVE_PATH, exist_ok=True)
    with open(TEST_PROFILE_CONFIGURATION_RELATIVE_PATH, "wt", encoding=TEXT_ENCODING) as config_file:
        config_file.write(TEST_PROFILE_CONFIGURATION_CONTENTS)
    with open(TEST_PLAYLIST_RELATIVE_PATH, "wt", encoding=TEXT_ENCODING) as playlist_file:
        playlist_file.write(TEST_PLAYLIST_FILE_CONTENTS)

    profile = Profile(TEST_PROFILE_NAME)
    configuration = Configuration(profile, TEST_PROFILE_CONFIGURATION_RELATIVE_PATH)
    mock_interface = InterfaceMock()
    _fill_profile_with_metadata(configuration, mock_interface)

    playlist = Playlist()
    file_extension = '.mp3'
    with open(TEST_PLAYLIST_RELATIVE_PATH, "rt", encoding=TEXT_ENCODING) as playlist_file:
        for line in playlist_file:
            audio_metadata = plain_text_parse._playlist_line_to_audio_metadata(line)
            audio_name = audio_loader.sanitize_filename(audio_metadata.name)
            print(audio_name)
            youtube_videos_metadatas = youtube_metadata_parser.search_videos_on_youtube(audio_name)
            maybe_chosen_youtube_video = audio_loader._get_first_youtube_search(youtube_videos_metadatas)
            audio_download_absolute_path = youtube_download.download_audio_from_youtube(
                youtube_url=maybe_chosen_youtube_video.url,
                output_directory_relative_path=configuration.get_audios_directory_path()
            )
            renamed_filepath = audio_loader._rename_filename(
                source_filepath=audio_download_absolute_path,
                new_filename=audio_name + file_extension
            )
            playlist.audios.append(Audio(
                name=audio_name,
                filepath=renamed_filepath,
                file_extension=file_extension
            ))

    yield {
        'profile': profile,
        'configuration_path': TEST_PROFILE_CONFIGURATION_RELATIVE_PATH,
        'playlist_path': TEST_PLAYLIST_RELATIVE_PATH,
        'playlist': playlist
    }

    # Teardown
    shutil.rmtree(TEST_CACHED_AUDIO_DIRECTORY_PATH)
