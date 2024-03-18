from audio.file_extension import FileExtension

class Audio: 
    """Audio file metadata representation class"""
    def __init__(self, name: str, filepath: str, file_extension: FileExtension):
        self.name: str = name
        self.filepath: str = filepath
        self.extension: str = file_extension
        self.lyrics_filepath: str = None

    def __str__(self) -> str:
        return f"Audio named \"{self.name}\" at {self.filepath}"

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if self is other:
            return True
        if isinstance(other, type(self)):
            return False
        return self.name == other.name and self.filepath == other.filepath and self.extension == other.extension
