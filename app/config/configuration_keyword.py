import enum

DEFAULT_PLAYLIST_PROFILE_NAME = "default"
GLOBAL_APP_SETTINGS_NAME = "global-settings"

class ConfigurationKeyword(enum.Enum):
    '''Enum class representing app's configuration setttings keywords'''
    # Global setting
    AUTO_IMPORT_DEFAUT_PLAYLIST_ON_STARTUP = "default-profile-import-on-startup"
    # Profile settings
    PLAYLIST_PATH = "playlist-file-relative-path"
    CACHE_DIRECTORY_PATH = "download-directory-relative-path"
    KEEP_CACHE_POLICY = "persistant-audio-cache"
    PREPARE_LYRICS_ON_IMPORT = "music-lyrics-search-on-import"
    USER_CHOOSES_AUDIO_SOURCE_ON_IMPORT = "audio-source-selection-on-import"
