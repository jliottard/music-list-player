from typing import List

class AudioMetadata():
    """ Class representing the audio information in the plain text"""

    def __init__(self, name: str, author: str | None, source: str | None, tags: List[str]):
        self.name: str = name
        self.author: str | None = author
        self.source: str | None = source    # at most one source (for now it is a web link but could be a local filepath)
        self.tags: List[str] = tags        # multiple, one or none tags but always a list

    def __eq__(self, other: object):
        are_equal = self.name == other.name
        are_equal &= self.author == other.author
        are_equal &= self.source == other.source
        for self_tag, other_tag in zip(self.tags, other.tags):
            are_equal &= self_tag == other_tag
        return are_equal

    def __str__(self):
        return f"AudioMetadata:[name:{self.name}, author:{self.author}, source:{self.source}, tag:{self.tags}]"