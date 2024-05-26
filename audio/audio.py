from audio.file_extension import FileExtension

class Audio:
    """Audio file metadata representation class"""
    def __init__(self, name: str, filepath: str, file_extension: FileExtension):
        self.name: str = name
        self.filepath: str = filepath
        self.extension: FileExtension = file_extension
        self.lyrics_filepath: str = None

    def __str__(self) -> str:
        return f"Audio named \"{self.name}\" at {self.filepath}"

    def debug(self) -> str:
        return f"Audio(name:{self.name}, filepath:{self.filepath}, extension: {self.extension}, lyrics_filepath: {self.lyrics_filepath})"

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        sames_attributes = [
            self.name == other.name,
            self.filepath == other.filepath,
            self.extension == other.extension
        ]
        return all(sames_attributes)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
