from typing import List
from app import configuration
from app.interface import Interface

def parse_plain_text_playlist_file(playlist_file_absolute_path: str, user_interface: Interface) -> List[str]:
    """Parse the plain text playlist file into a list of musics
        @param playlist_file_absolute_path: str the file path to the plain text file
        @param user_interface: Interface
        @return List[str]: the musics' names
    """
    user_interface.request_output_to_user("Info: parsing playlist file.")
    with open(playlist_file_absolute_path, "rt", encoding=configuration.TEXT_ENCODING) as playlist_file:
        lines = playlist_file.readlines()
        def remove_carriage_return(string):
            return string.strip("\n")
        return list(map(remove_carriage_return, lines))
