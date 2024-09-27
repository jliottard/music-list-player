import pytest

from app.config.configuration import Configuration
from app.config.profile import Profile
from test.conftest import setup_and_teardown_playlist_and_configuration_files

def test_profile_audio_metadatas_by_tag(setup_and_teardown_playlist_and_configuration_files):
    test_config = setup_and_teardown_playlist_and_configuration_files
    configuration: Configuration = test_config['configuration']
    profile: Profile = configuration.profile
    expected_tag = '#chopin'
    assert len(profile.audio_metadatas_by_tag(expected_tag)) != 0
