''' App's shutdown process '''

from app.config.configuration import Configuration
from app.interface import Interface
from app.message_priority import MessagePriority
from audio.audio_player import AudioPlayer
from audio_import.audio_loader import flush_playlist_cache

def clean_app_termination(
    player: AudioPlayer, configuration: Configuration | None, user_interface: Interface):
    """Delete memory and running app before shutting down the app
    @param player: AudioPlayer
    @param playlist_profile: Profile | None
    @param user_interface: Interface
    """
    player.stop()
    if configuration is None:
        return
    if not configuration.is_audio_cache_persistant():
        dir_path = configuration.get_audios_directory_path()
        user_interface.request_output_to_user(
            f"Info: Erasing saved audios from the \"{dir_path}\" directory.",
            MessagePriority.INFO
        )
        flush_playlist_cache(player.playlist, configuration)
