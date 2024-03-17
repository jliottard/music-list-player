#!/usr/bin/python3
import sys

from typing import List

from app import configuration, interface
from app.actions.help import print_help
from app.actions.import_playlist import import_playlist
from app.actions.list import print_list
from app.actions.lyric import request_lyrics
from app.actions.mode import request_mode
from app.actions.next import skip_music
from app.actions.play import play
from app.actions.shuffle import shuffle_playlist
from app.actions.volume import request_volume
from app.command import Command, parse_command
from app.termination import clean_app_termination
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist
from lyrics.lyrics_displayer import LyricsDisplayer

def setup() -> bool:
    """ Check app initialization """
    if not configuration.check_required_files_from_configuration_exist():
        return False
    return True

if __name__ == "__main__":
    if not setup():
        print("Error while app initialization.")
        sys.exit()
    player = AudioPlayer(Playlist(), AudioPlayer.AUDIO_VOLUME_BASE)
    lyrics_displayer = LyricsDisplayer(player)
    profile = configuration.DEFAULT_PLAYLIST_PROFILE_NAME
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
                clean_app_termination(player, profile)
                print("Goodbye!")
                break
            case Command.HELP:
                print_help()
            case Command.IMPORT:
                player, profile = import_playlist(maybe_args, player)
                lyrics_displayer = LyricsDisplayer(player)
            case Command.LIST:
                print_list(player)
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
                request_mode(maybe_args, player)
            case Command.VOLUME:
                request_volume(maybe_args, player)
            case Command.LYRIC:
                request_lyrics(maybe_args, lyrics_displayer)
            case _:
                pass
