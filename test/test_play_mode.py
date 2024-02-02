from audio import play_mode

def test_every_play_mode_enum_string():
    for tested_mode in play_mode.PlayMode:
        assert isinstance(str(tested_mode), str)

def test_every_play_mode_from_string():
    for tested_mode in play_mode.PlayMode:
        assert isinstance(play_mode.from_string(str(tested_mode)), play_mode.PlayMode)
