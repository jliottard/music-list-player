import os
import pytest

from app.actions.change_profile import _fill_profile_with_metadata
from app.config.configuration import Configuration, TEXT_ENCODING
from app.config.profile import Profile
from audio.playlist import Playlist
from test.interface_mock import InterfaceMock

TEST_WORK_DIRECTORY_RELATIVE_PATH = "test"

TEST_PLAYLIST_RELATIVE_PATH = os.path.join(
    TEST_WORK_DIRECTORY_RELATIVE_PATH,
    "playlist_for_test.txt"
)
TEST_PLAYLIST_FILE_CONTENTS = "\n".join(
    [
        'nocturne op. 55 no. 1 by frédéric chopin #chopin',
        'nocturne op.9 no.2 by frédéric chopin #chopin',
        'etude op 10 no.4 by frédéric chopin #chopin (https://www.youtube.com/watch?v=oHiU-u2ddJ4)'
        'hungarian dance no. 5 by johannes brahms'
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
    with open(TEST_PROFILE_CONFIGURATION_RELATIVE_PATH, "at", encoding=TEXT_ENCODING) as config_file:
        config_file.write(TEST_PROFILE_CONFIGURATION_CONTENTS)
    with open(TEST_PLAYLIST_RELATIVE_PATH, "at", encoding=TEXT_ENCODING) as playlist_file:
        playlist_file.write(TEST_PLAYLIST_FILE_CONTENTS)

    profile = Profile(TEST_PROFILE_NAME)
    configuration = Configuration(profile, TEST_PROFILE_CONFIGURATION_RELATIVE_PATH)
    mock_interface = InterfaceMock()
    _fill_profile_with_metadata(profile, mock_interface)

    with open(TEST_PLAYLIST_RELATIVE_PATH, "at", encoding=TEXT_ENCODING) as playlist_file:
        for line in playlist_file:
            pass # TODO load audios into playlist

    youtube_videos_metadatas: List[YouTubeVideoMetadata] = youtube_metadata_parser.search_videos_on_youtube(audio_name)
    maybe_chosen_youtube_video: YouTubeVideoMetadata | None = _get_first_youtube_search(youtube_videos_metadatas)
    audio_download_absolute_path = youtube_download.download_audio_from_youtube(
        youtube_url=maybe_chosen_youtube_video.url,
        output_directory_relative_path=configuration.get_audios_directory_path()
    )
    playlist = Playlist()

    yield {
        'profile': profile,
        'configuration_path': TEST_PROFILE_CONFIGURATION_RELATIVE_PATH,
        'playlist_path': TEST_PLAYLIST_RELATIVE_PATH,
        'playlist': playlist
    }

    # Teardown
    for file_for_test in [TEST_PROFILE_CONFIGURATION_RELATIVE_PATH, TEST_PLAYLIST_RELATIVE_PATH]:
        os.remove(file_for_test)
    os.rmdir(TEST_CACHED_AUDIO_DIRECTORY_PATH)
