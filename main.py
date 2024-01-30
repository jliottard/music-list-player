#!/usr/bin/python3
import sys
from typing import List

from app.command import Command
from app import configuration
from audio.playlist import Playlist
from audio.audio_player import AudioPlayer
from audio.play_mode import PlayMode, from_string
from audio import audio_loader
from cannot_find_a_match_error import CannotFindAMatchError

def setup() -> bool:
    # Check app initialization
    if not configuration.check_required_files_from_configuration_exist():
        return False
    return True

def parse_command(command_input: str) -> list:
    # Parse the inputed by user command
    # Return:
    # - a list of the command arguments with the first argument as a Command element
    # - None if the command is not recognized
    def is_not_empty(e) -> bool:
        return e != ""
    args = list(filter(is_not_empty, command_input.split(" ")))
    first_argument = args[0]
    for command in Command:
        if first_argument == command.value:
            args[0] = command
    if type(args[0]) == type(""):
        return None
    return args

def match_string_among_strings(searched_string: str, strings: List[str]) -> int:
    # Search a matching searched_name among strings
    # Exception: raise a CannotFindAMatchError if there is no match
    for index, string in enumerate(strings):
        if searched_string.lower() in string.lower():
            return index
    decomposed_string = searched_string.split(" ")
    for sub_string_component in range(decomposed_string):
        for index, string in enumerate(strings):
            if sub_string_component.lower() in string.lower():
                return index
    raise CannotFindAMatchError

def match_some_strings_among_strings(searched_arguments: List[str], expected_arguments: List[str]) -> int:
    # @exception: raise a CannotFindAMatchError if there is no match
    for searched_argument in searched_arguments:
        for index, expected_argument in enumerate(expected_arguments):
            if searched_argument.lower() in expected_argument:
                return index
    raise CannotFindAMatchError

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    player = AudioPlayer(Playlist())
    print("Welcome to music list player! Please enter a command (type: \"help\" for help).")
    while True:
        user_input_command: str = input()
        maybe_args: List[str] = parse_command(user_input_command)
        if maybe_args is None:
            print(f"\"{user_input_command}\" command is unknown.")
            continue
        match maybe_args[0]:
            case Command.QUIT:
                print("Goodbye!")
                break
            case Command.HELP:
                print(f"The available commands are :")
                for command in list(Command):
                    help = command.help()
                    print(f"- {command.value:10s}\t{help}")
            case Command.IMPORT:
                player.stop()
                playlist_path = configuration.get_playlist_file_path()
                playlist = Playlist()
                playlist.audios = audio_loader.load(playlist_file_absolute_path=playlist_path)
                player = AudioPlayer(playlist)
            case Command.LIST:
                print("Music list:")
                maybe_played_audio = player.get_playing_audio()
                for index, audio in enumerate(playlist.audios):
                    if maybe_played_audio is not None and audio == maybe_played_audio:
                        print(f"- ({index}) {audio.name} \t\t (currently playing)")
                    else:
                        print(f"- ({index}) {audio.name}")
            case Command.PLAY:
                if len(maybe_args) == 2:
                    try:
                        second_argument = maybe_args[1]
                        audio_index = int(second_argument)
                    except ValueError as value_error:
                        print(f"Unexpected argument provided: \"{second_argument}\", it was expected to be the index of the audio in the playlist (integer).")
                        continue
                    if not player.play_audio_at_index(audio_index):
                        print(f"Cannot find the \"{audio_index}\" index in the playlist.")
                        continue
                elif len(maybe_args) > 2:
                    try:
                        audio_name_to_play = " ".join(maybe_args[1:])
                    except ValueError as value_error:
                        print(f"Unexpected arguments provided: \"{arguments}\", it was expected to be a audio name (string).")
                        continue
                    try:
                        audio_to_play_index = match_string_among_strings(audio_name_to_play, player.playlist.names())
                    except CannotFindAMatch as cannot_find_a_match_error:
                        print(f"Cannot find a matching audio with \"{audio_name_to_play}\".")
                        continue
                    else:
                        if not player.play_audio_at_index(audio_to_play_index):
                            print(f"Audio match found but cannot find its \"{audio_index}\" index in the playlist.")
                        continue
                else:
                    player.play()
                maybe_played_audio = player.get_playing_audio()
                if maybe_played_audio is None:
                    print("Playing..")
                else:
                    print(f"Playing \"{maybe_played_audio.name}\".")
            case Command.NEXT:
                maybe_playing_audio_index = player.get_playing_audio_index()
                if maybe_playing_audio_index is None:
                    next_audio_name = ".."
                else:
                    next_audio_index = (maybe_playing_audio_index + 1) % len(player.playlist.audios)
                    next_audio_name = player.playlist.names()[next_audio_index]
                is_playing_audio_last = player.get_playing_audio_index() == len(player.playlist.audios) - 1
                if is_playing_audio_last:
                    match player.get_play_mode():
                        case PlayMode.PLAYLIST_LOOP:
                            player.play_audio_at_index(0)
                        case PlayMode.ONE_PASS:
                            print("Cannot skip, end of playlist reached as one pass mode.")
                            continue
                        case _:
                            pass
                else:
                    player.next()
                print(f"Skipping to \"{next_audio_name}\".")
            case Command.STOP:
                player.stop()
                print("Stopping the audio.")
            case Command.PAUSE:
                if player.is_playing():
                    print("Pausing the audio.")
                    player.pause()
            case Command.RESUME:
                if not player.is_playing():
                    print("Resuming the audio.")
                    player.resume()
            case Command.SHUFFLE:
                current_audio = player.get_playing_audio()
                player.stop()
                print("Shuffling playlist.")
                player.shuffle()
                index = player.get_index_of_audio(current_audio)
                player.play_audio_at_index(index)
            case Command.MODE:
                if len(maybe_args) >= 2:
                    try:
                        MODES = [str(mode) for mode in PlayMode]
                        mode_index = match_string_among_strings(" ".join(maybe_args[1:]), MODES)
                        player.set_play_mode(from_string(MODES[mode_index]))
                    except CannotFindAMatchError as cannot_find_a_match_error:
                        print(f"Cannot find a matching mode with \"{audio_name_to_play}\".")
                        continue
                    else:
                        print(f"Setting play mode as {player.get_play_mode()}.")
                else:
                    print(f"Current play mode is {player.get_play_mode()}.")
            case _:
                pass
