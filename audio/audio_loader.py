import os

from app import configuration
from audio.audio import Audio
from audio import download
from audio.cannot_download_error import CannotDownloadError
from audio.file_extension import FileExtension

def load(playlist_file_absolute_path: str) -> list[Audio]:
    # Description: Parse playlist file
    # @param playlist_file_absolute_path a filepath of the text file describing the music playlist
    # @return a list of the audios
    playlist_lines: list[str] = []
    print("Parsing playlist file.")
    with open(playlist_file_absolute_path, "rt", encoding="utf-8") as playlist_file:
        playlist_lines = playlist_file.readlines()
    print("Checking local cache of audios.")
    audios: list[Audio] = []
    MP3_FILE_EXTENSION = FileExtension.MP3
    for audio_name in playlist_lines:
        audio_name = audio_name.strip("\n")
        audio_file_path: str = configuration.get_audio_file_path(audio_name + MP3_FILE_EXTENSION.value)
        if os.path.exists(audio_file_path):
            print(f"The audio \"{audio_name}\" is found in cache.")
            # print(f"Using audio cache located {audio_file_path}.") debug level
            audio: audio.Audio = Audio(name=audio_name, filepath=audio_file_path, file_extension=MP3_FILE_EXTENSION)
        else:
            print(f"The audio \"{audio_name}\" is not found in cache. Downloading audio from internet.")
            youtube_video_url: str = download.get_youtube_video_url(audio_name)
            try:
                audio_download_absolute_path = download.download_audio_from_youtube(
                    youtube_url=youtube_video_url,
                    output_directory_relative_path=configuration.get_audios_directory_path()
                )
            except CannotDownloadError as video_cannot_be_downloaded:
                print(f"Warning: the video {audio_name} could not be downloaded due to {video_cannot_be_downloaded.args}")
                continue
            # Rename the file having Youtube video title as name to the audio name
            #  from the playlist file
            drive, path_and_file = os.path.splitdrive(audio_download_absolute_path)
            path, file = os.path.split(path_and_file)
            playlist_name_like_audio_absolute_path = os.path.join(path, audio_name + MP3_FILE_EXTENSION.value)
            os.rename(audio_download_absolute_path, playlist_name_like_audio_absolute_path)
            print("playlist_name_like_audio_absolute_path", playlist_name_like_audio_absolute_path)
            audio = Audio(name=audio_name, filepath=playlist_name_like_audio_absolute_path, file_extension=MP3_FILE_EXTENSION)
        audios.append(audio)
    return audios
