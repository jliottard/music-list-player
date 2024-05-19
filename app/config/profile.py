from typing import List

from app.config.configuration_keyword import DEFAULT_PLAYLIST_PROFILE_NAME
from audio_import.audio_metadata import AudioMetadata


class Profile():
    """ TODO write a description """

    def __init__(self, name: str = DEFAULT_PLAYLIST_PROFILE_NAME):
        self.name: str = name
        self.audio_metadatas: List[AudioMetadata] = []
        

    def audio_metadatas_by_tag(self, tag: str):
        """Return a list of the audio metadatas with the given tag
        @param tag: str
        @return List[AudioMetadata]
        """
        tagged_audio_metadata = []
        for metadata in self.audio_metadatas:
            if tag in metadata.tags:
                tagged_audio_metadata.append(metadata)
        return tagged_audio_metadata
