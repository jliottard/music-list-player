from typing import List

class AudioMetadata():
    """ Class representing the audio information in the plain text"""

    def __init__(self, name: str, author: str, source: str, tags: List[str]):
        self.name = name
        self.author = author
        self.source = source    # at most, one source (for now it is a web link but could be a local filepath)
        self.tags = tags        # multiple or none tags
