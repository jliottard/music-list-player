#!/usr/bin/python3
import sys

from typing import List

from app.actions.help import print_help
from app.actions.import_playlist import import_playlist
from app.actions.list import print_list
from app.actions.lyric import request_lyrics
from app.actions.mode import request_mode
from app.actions.move_timeline import request_move
from app.actions.next import skip_music
from app.actions.change_profile import request_profile
from app.actions.play import play
from app.actions.shuffle import shuffle_playlist
from app.actions.volume import request_volume
from app.command import Command, parse_command
from app.config.configuration import Configuration
from app.config.configuration_keyword import DEFAULT_PLAYLIST_PROFILE_NAME
from app.config.profile import Profile
from app.interface import Interface
from app.termination import clean_app_termination
from audio.audio_player import AudioPlayer
from audio.playlist import Playlist
from lyrics.lyrics_displayer import LyricsDisplayer

def setup(configuration: Configuration) -> bool:
    """ Check app initialization """
    if not configuration.check_required_files_from_configuration_exist():
        return False
    return True

if __name__ == "__main__":
    user_interface = Interface()
    player = AudioPlayer(Playlist(), AudioPlayer.AUDIO_VOLUME_BASE)
    lyrics_displayer = LyricsDisplayer(player, user_interface)
    profile: Profile = Profile(DEFAULT_PLAYLIST_PROFILE_NAME)
    configuration = Configuration(profile)
    try:
        setup(configuration)
    except Exception as e:
        user_interface.request_output_to_user(
            f"Error while app initialization. More details: {e}"
        )
        sys.exit()
    user_interface.request_output_to_user("Info: Welcome to music list player!")
    if configuration.is_default_profile_imported_on_startup():
        user_interface.request_output_to_user("Info: Auto-import on startup..")
        player: AudioPlayer | None = import_playlist(parse_command(Command.IMPORT.value), configuration, player, user_interface)
        lyrics_displayer = LyricsDisplayer(player, user_interface)
    user_interface.request_output_to_user(f"Request: Please enter a command (type: \"{Command.HELP.value}\" for help).")
    while True:
        user_input_command: str = user_interface.request_input_from_user()
        user_interface.update_app_display(player)
        maybe_played_audio = player.get_playing_audio()
        maybe_args: List[str] = parse_command(user_input_command)
        if maybe_args is None:
            user_interface.request_output_to_user(f"\"{user_input_command}\" command is unknown.")
            continue
        match maybe_args[0]:
            case Command.QUIT:
                clean_app_termination(player, configuration, user_interface)
                user_interface.request_output_to_user("Goodbye!")
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
                user_interface.request_output_to_user("Stopping the audio.")
            case Command.PAUSE:
                if player.is_playing():
                    user_interface.request_output_to_user("Pausing the audio.")
                    player.pause()
            case Command.RESUME:
                if not player.is_playing():
                    user_interface.request_output_to_user("Resuming the audio.")
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
            case _:
                pass
