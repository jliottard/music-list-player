from audio import playlist
from audio import audio
from audio import file_extension

from test.conftest import AUDIO_FILE_EXTENSION

def test_playlist_names_order():
    tested_playlist = playlist.Playlist()
    audios = []
    expected_names = []
    for i in range(10):
        audio_name = "audio" + str(i)
        audio_path = "path/to/" + audio_name
        audios.append(
            audio.Audio(audio_name, audio_path, AUDIO_FILE_EXTENSION)
        )
        expected_names.append(audio_name)
    tested_playlist.audios = audios
    for name, expected_name in zip(tested_playlist.names(), expected_names):
        assert name == expected_name
