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

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    playlist = Playlist()
    player = AudioPlayer(playlist)
    print("Welcome to music list player! Please enter a command (type: \"help\" for help).")
    while True:
        user_input_command = input()
        # todo: pre-parser for security?
        #command = parse_command(user_input_command)
        if user_input_command == Command.QUIT.value:
            print("Goodbye!")
            break
        elif user_input_command == Command.HELP.value:
            print(f"The commands available are :") 
            for command in list(Command):
                help = command.help()
                print(f"- {command.value}\t{help}")
        elif user_input_command == Command.IMPORT.value:
            playlist_path = configuration.get_playlist_file_path()
            playlist.audios = audio_loader.load(playlist_file_absolute_path=playlist_path)
            del(player)
            player = AudioPlayer(playlist)
        elif user_input_command == Command.LIST.value:
            print("Music list:")
            for index, audio in enumerate(playlist.audios):
                if index == playlist.current_audio_index:
                    print(f"- {audio.name} (currently playing)")
                else:
                    print(f"- {audio.name}")
        elif user_input_command == Command.PLAY.value:
            player.play()
            print(f"Playing \"{player.playlist.current_audio().name}\" audio.")
        elif user_input_command == Command.NEXT.value:
            player.next()
            print(f"Skiping to next audio:{player.playlist.current_audio().name}")
        elif user_input_command == Command.STOP.value:
            player.stop()
            print("Stopping the audio.")
        elif user_input_command == Command.PAUSE.value:
            player.pause()
            if player.is_playing():
                print("Pausing the audio.")
            else:
                print("Resuming the audio.")
        else:
            print(f"{user_input_command} command is unknown.")

