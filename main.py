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
            maybe_played_audio = player.get_playing_audio()
            for index, audio in enumerate(playlist.audios):
                if maybe_played_audio is not None and audio == maybe_played_audio:
                    print(f"- ({index}) {audio.name} \t\t (currently playing)")
                else:
                    print(f"- ({index}) {audio.name}")
        elif user_input_command == Command.PLAY.value:
            player.play()
            maybe_played_audio = player.get_playing_audio()
            if maybe_played_audio is None:
                print("Nothing to play.")
            else:
                print(f"Playing {maybe_played_audio.name}.")
        elif user_input_command == Command.NEXT.value:
            player.next()
            maybe_played_audio = player.get_playing_audio()
            if maybe_played_audio is None:
                print("Skip impossible.")
            else:
                print(f"Skipping to {maybe_played_audio.name}")
        elif user_input_command == Command.STOP.value:
            player.stop()
            print("Stopping the audio.")
        elif user_input_command == Command.PAUSE.value:
            if player.is_playing():
                print("Pausing the audio.")
                player.pause()
        elif user_input_command == Command.RESUME.value:
            if not player.is_playing():
                print("Resuming the audio.")
                player.resume()
        elif user_input_command == Command.SHUFFLE.value:
            current_audio = player.get_playing_audio()
            player.stop()
            print("Shuffling playlist.")
            player.shuffle()
            index = player.get_index_of_audio(current_audio)
            player.play_audio_at_index(index)
        elif user_input_command == Command.LOOP.value:
            print("Setting play mode as loop.")
            player.set_loop()
        elif user_input_command == Command.UNLOOP.value:
            print("Setting play mode as default")
            player.set_default()
        else:
            print(f"\"{user_input_command}\" command is unknown.")

