#!/usr/bin/python3
import sys
from typing import List

from app.command import Command
from app import configuration
from audio.playlist import Playlist
from audio.audio_player import AudioPlayer
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

def match(searched_name: str, names: List[str]) -> int:
    # Search a matching searched_name amoung names
    # Exception: raise a CannotFindAMatchError if there is no match
    for index, name in enumerate(names):
        if searched_name.lower() in name.lower():
            return index
    decomposed_name = searched_name.split(" ")
    for sub_name_component in range(decomposed_name):
        for index, name in enumerate(names):
            if sub_name_component.lower() in name.lower():
                return index
    raise CannotFindAMatchError

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    playlist = Playlist()
    player = AudioPlayer(playlist)
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
                playlist_path = configuration.get_playlist_file_path()
                playlist.audios = audio_loader.load(playlist_file_absolute_path=playlist_path)
                del(player)
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
                if len(maybe_args) > 2:
                    try:
                        arguments = maybe_args[1]
                        audio_name_to_play = str(arguments)
                    except ValueError as value_error:
                        print(f"Unexpected arguments provided: \"{arguments}\", it was expected to be a audio name (string).")
                        continue
                    try:
                        audio_to_play_index = match(audio_name_to_play, playlist.names())
                    except CannotFindAMatch as cannot_find_a_match_error:
                        print(f"Cannot find a matching audio with \"{audio_name_to_play}\".")
                        continue
                    else:
                        if not player.play_audio_at_index(audio_to_play_index):
                            print(f"Audio match found but cannot find its \"{audio_index}\" index in the playlist.")
                        continue
                player.play()
                maybe_played_audio = player.get_playing_audio()
                if maybe_played_audio is None:
                    print("Nothing to play.")
                else:
                    print(f"Playing {maybe_played_audio.name}.")
            case Command.NEXT:
                player.next()
                maybe_played_audio = player.get_playing_audio()
                if maybe_played_audio is None:
                    print("Skip impossible.")
                else:
                    print(f"Skipping to {maybe_played_audio.name}")
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
            case Command.LOOP:
                print("Setting play mode as loop.")
                player.set_loop()
            case Command.UNLOOP:
                print("Setting play mode as default")
                player.set_default()
            case _:
                pass
