from app.configuration import is_audio_cache_persistant, get_audios_directory_path
from app.interface import Interface
from audio.audio_player import AudioPlayer
from audio_import.audio_loader import flush_playlist_cache

def clean_app_termination(player: AudioPlayer, playlist_profile: str, user_interface: Interface):
    """Delete memory and running app before shutting down the app
    @param player: AudioPlayer
    @param playlist_profile: str
    @param user_interface: Interface
    """
    player.stop()
    if not is_audio_cache_persistant(playlist_profile):
        user_interface.request_output_to_user(
            f"Erasing saved audios from the \"{get_audios_directory_path(playlist_profile)}\" directory."
        )
        flush_playlist_cache(player.playlist, playlist_profile)
