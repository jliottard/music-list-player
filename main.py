#!/usr/bin/python3
import sys

from typing import List, Tuple

from app.actions.help import print_help
from app.actions.import_playlist import import_playlist
from app.actions.list import print_list
from app.actions.lyric import request_lyrics
from app.actions.mode import request_mode
from app.actions.move_timeline import request_move
from app.actions.mute import mute, unmute
from app.actions.next import skip_music
from app.actions.change_profile import request_profile
from app.actions.play import play
from app.actions.shuffle import shuffle_playlist
from app.actions.volume import request_volume
from app.command import Command, parse_command
from app.config.configuration import Configuration, CONFIGURATION_FILE_PATH
from app.config.profile import Profile
from app.interface import Interface
from app.message_priority import MessagePriority
from app.termination import clean_app_termination
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist
from lyrics.lyrics_displayer import LyricsDisplayer

def check_configuration(configuration: Configuration, user_interface: Interface) -> bool:
    '''Check application's configuration
    @return: bool, True if the configuration is correct, False if something is missing.
    '''
    missing_filepaths: List[str] = configuration.search_missing_but_required_files_from_configuration_exist()
    if missing_filepaths:
        user_interface.request_output_to_user(
            f"Error: The following filepath(s) defined in the {CONFIGURATION_FILE_PATH} file do not exist:",
            MessagePriority.ERROR
        )
        for missing_filepath in missing_filepaths:
            user_interface.request_output_to_user(
                f"{missing_filepath}",
                MessagePriority.ERROR
            )
        return False
    if not configuration.check_default_profile_is_defined_in_configuration():
        user_interface.request_output_to_user(
            f"Error: The default profile named \"{configuration.get_default_profile_name()}\" is not defined in the {CONFIGURATION_FILE_PATH} file",
            MessagePriority.ERROR
        )
        return False
    return True

def init() -> Tuple[Configuration, Interface, AudioPlayer, LyricsDisplayer]:
    '''Check the configuration and load any initialization states that are needed
    @returns Configuration, Interface, AudioPlayer, LyricsDisplayer
    '''
    user_interface = Interface()
    user_interface.request_output_to_user("Info: Welcome to music list player!", MessagePriority.INFO)
    player = AudioPlayer(Playlist(), AudioPlayer.AUDIO_VOLUME_BASE)
    lyrics_displayer = LyricsDisplayer(player, user_interface)
    configuration = Configuration(profile=None)
    is_configuration_valid = False
    try:
        is_configuration_valid = check_configuration(configuration, user_interface)
    except Exception:
        pass
    finally:
        if not is_configuration_valid:
            user_interface.request_output_to_user(
                "Info: Application's initialization failed! Exiting application..",
                MessagePriority.INFO
            )
            sys.exit()
    configuration.fill_profile_with_metadata(user_interface)
    if configuration.is_default_profile_imported_on_startup():
        user_interface.request_output_to_user("Info: Auto-import on startup..", MessagePriority.INFO)
        player: AudioPlayer | None = import_playlist(parse_command(Command.IMPORT.value), configuration, player, user_interface)
        lyrics_displayer = LyricsDisplayer(player, user_interface)
    return configuration, user_interface, player, lyrics_displayer

def loop(configuration: Configuration, user_interface: Interface, player: AudioPlayer, lyrics_displayer: LyricsDisplayer):
    '''Loop over the commands of the user
    @param configuration: Configuration
    @param user_interface: Inteface
    @param player: AudioPlayer
    @param lyrics_displayer: LyricsDisplayer
    '''
    user_interface.request_output_to_user(f"Request: Please enter a command (type: \"{Command.HELP.value}\" for help).", MessagePriority.INFO)
    while True:
        user_input_command: str = user_interface.request_input_from_user()
        user_interface.update_app_display(player)
        maybe_args: List[str] = parse_command(user_input_command)
        if maybe_args is None:
            user_interface.request_output_to_user(f"Warning: \"{user_input_command}\" command is unknown.", MessagePriority.INFO)
            continue
        match maybe_args[0]:
            case Command.QUIT:
                clean_app_termination(player, configuration, user_interface)
                user_interface.request_output_to_user("Info: Goodbye!", MessagePriority.INFO)
                break
            case Command.HELP:
                print_help(user_interface)
            case Command.IMPORT:
                player: AudioPlayer | None = import_playlist(maybe_args, configuration, player, user_interface)
                lyrics_displayer = LyricsDisplayer(player, user_interface)
            case Command.LIST:
                print_list(player, user_interface)
            case Command.PLAY:
                play(maybe_args, player, user_interface)
            case Command.NEXT:
                skip_music(player, user_interface)
            case Command.STOP:
                player.stop()
                user_interface.request_output_to_user("Info: Stopping the audio.", MessagePriority.INFO)
            case Command.PAUSE:
                if player.is_playing():
                    user_interface.request_output_to_user("Info: Pausing the audio.", MessagePriority.INFO)
                    player.pause()
            case Command.RESUME:
                if not player.is_playing():
                    user_interface.request_output_to_user("Info: Resuming the audio.", MessagePriority.INFO)
                    player.resume()
            case Command.SHUFFLE:
                shuffle_playlist(player, user_interface)
            case Command.MODE:
                request_mode(maybe_args, player, user_interface)
            case Command.VOLUME:
                request_volume(maybe_args, player, user_interface)
            case Command.LYRIC:
                request_lyrics(maybe_args, lyrics_displayer)
            case Command.MOVE:
                request_move(maybe_args, player)
            case Command.PROFILE:
                configuration.profile: Profile | None = request_profile(maybe_args, configuration, user_interface)
            case Command.MUTE:
                print("command mute")
                mute(maybe_args, user_interface)
            case Command.UNMUTE:
                unmute(maybe_args, user_interface)
            case _:
                pass

def main():
    '''Application entry point'''
    loop(*init())

if __name__ == "__main__":
    main()
