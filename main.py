#!/usr/bin/python3
import os
import sys
from typing import List

from app import configuration
from app.actions.help import print_help
from app.actions.import_playlist import import_defaut_playlist
from app.actions.list import print_list
from app.actions.mode import define_mode
from app.actions.next import skip_music
from app.actions.play import play
from app.actions.shuffle import shuffle_playlist
from app.command import Command, parse_command
from app import interface
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist

def setup() -> bool:
    """ Check app initialization """
    if not configuration.check_required_files_from_configuration_exist():
        return False
    return True

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    player = AudioPlayer(Playlist())
    print(f"Welcome to music list player! Please enter a command (type: \"{str(Command.HELP)}\" for help).")
    while True:
        user_input_command: str = input()
        interface.update_terminal(player)
        maybe_played_audio = player.get_playing_audio()
        maybe_args: List[str] = parse_command(user_input_command)
        if maybe_args is None:
            print(f"\"{user_input_command}\" command is unknown.")
            continue
        match maybe_args[0]:
            case Command.QUIT:
                print("Goodbye!")
                break
            case Command.HELP:
                print_help()
            case Command.IMPORT:
                playlist, player = import_defaut_playlist(player)
            case Command.LIST:
                print_list(playlist, player)
            case Command.PLAY:
                play(maybe_args, player)
            case Command.NEXT:
                skip_music(player)
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
                shuffle_playlist(player)
            case Command.MODE:
                define_mode(maybe_args, player)
            case _:
                pass
