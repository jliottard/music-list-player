from app import command
def test_parse_command_on_every_command_keyword():
    for expected_command_enum in command.Command:
        testing_command = str(expected_command_enum)
        tested_first_arg = command.parse_command(testing_command)[0]
        assert tested_first_arg == expected_command_enum

def test_parse_command_with_unknown_command_keyword():
    assert command.parse_command("") is None
