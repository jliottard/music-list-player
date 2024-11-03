from app.path import operating_system_proof_path
from audio.file_extension import FileExtension

class Audio:
    """Audio file metadata representation class"""
    def __init__(self, name_without_extension: str, filepath: str, file_extension: FileExtension):
        self.name_without_extension: str = name_without_extension
        self.filepath: str = filepath
        self.extension: FileExtension = file_extension
        self.lyrics_filepath: str = None

    def __str__(self) -> str:
        return f"Audio named \"{self.name_without_extension}\" at {self.filepath}"

    def debug(self) -> str:
        return f"Audio(name: {self.name_without_extension}, filepath: {self.filepath}, extension: {self.extension}, lyrics_filepath: {self.lyrics_filepath})"

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        sames_attributes = [
            self.name_without_extension == other.name_without_extension,
            operating_system_proof_path(self.filepath) == operating_system_proof_path(other.filepath),
            self.extension == other.extension,
            self.lyrics_filepath == other.lyrics_filepath
        ]
        return all(sames_attributes)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
