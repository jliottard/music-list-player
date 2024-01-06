from audio.file_extension import FileExtension

class Audio:
    def __init__(self, name: str, filepath: str, file_extension: FileExtension):
        self.name = name
        self.filepath = filepath
        self.extension = file_extension

    def __str__(self) -> str:
        return f"Audio named \"{self.name}\" at {self.filepath}"
