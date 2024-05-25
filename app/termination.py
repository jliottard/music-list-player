from app.config.configuration import Configuration
from app.interface import Interface
from audio.audio_player import AudioPlayer
from audio_import.audio_loader import flush_playlist_cache

def clean_app_termination(player: AudioPlayer, configuration: Configuration | None, user_interface: Interface):
    """Delete memory and running app before shutting down the app
    @param player: AudioPlayer
    @param playlist_profile: Profile | None
    @param user_interface: Interface
    """
    player.stop()
    if configuration is None:
        return
    if not configuration.is_audio_cache_persistant():
        user_interface.request_output_to_user(
            f"Erasing saved audios from the \"{configuration.get_audios_directory_path()}\" directory."
        )
        flush_playlist_cache(player.playlist, configuration)
