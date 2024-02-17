from app.configuration import is_audio_cache_persistant, get_audios_directory_path
from audio.audio_player import AudioPlayer
from audio.file_import.audio_loader import flush_playlist_cache

def clean_app_termination(player: AudioPlayer, playlist_profile: str):
    ''' Delete memory and running app before shutting down the app '''
    player.stop()
    if not is_audio_cache_persistant(playlist_profile):
        print(f"Erasing saved audios from the \"{get_audios_directory_path(playlist_profile)}\" directory.")
        flush_playlist_cache(player.playlist, playlist_profile)
