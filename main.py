#!/usr/bin/python3
import sys

from app.command import Command
from app import configuration
from audio.playlist import Playlist
from audio.audio_player import AudioPlayer
from audio import audio_loader

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

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    playlist = Playlist()
    player = AudioPlayer(playlist)
    print("Welcome to music list player! Please enter a command (type: \"help\" for help).")
    while True:
        user_input_command = input()
        maybe_args = parse_command(user_input_command)
        if maybe_args is None:
            print(f"\"{user_input_command}\" command is unknown.")
            continue
        match maybe_args[0]:
            case Command.QUIT:
                print("Goodbye!")
                break
            case Command.HELP:
                print(f"The commands available are :")
                for command in list(Command):
                    help = command.help()
                    print(f"- {command.value}\t{help}")
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
