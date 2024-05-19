from typing import List
import re
from app.config.configuration import TEXT_ENCODING
from app.interface import Interface
from audio_import.audio_metadata import AudioMetadata

SPACE = ' '

def remove_carriage_return(string):
    """ Just remove starting or ending carriage return"""
    return string.strip("\n")

def try_extract_web_url(audio_line: str) -> str | None:
    """Parse the line and extract any web url in it
        @param audio_line: str
        @return str | None: the url or nothing
    """
    URL_REGEX = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    maybe_regex_match = re.search(
        URL_REGEX,
        audio_line
    )
    if maybe_regex_match is None:
        return None
    return maybe_regex_match.group(0)

def try_extract_tags(audio_line: str) -> List[str]:
    """ Parse the line and extract any tags in it
        @param audio_line: str
        @return: List[str], empty list if there is no tag found
    """
    TAG_REGEX = r'#[a-zA-Z0-9_\-]+'
    return re.findall(TAG_REGEX, audio_line)

def _is_there_one_space_before_substring(string: str, substring: str) -> bool:
    """ Return True if there is a space just before the given substring in string """

    return string[max(0, string.find(substring)-1)] == SPACE

def remove_metadata(audio_line: str) -> str:
    """ Remove the meta data from the line
        @param audio_line: str
        @return: str
    """
    EXPECTED_SOURCE_SEPARATION = ' '
    purged_line = audio_line
    # Remove tags
    any_tags = try_extract_tags(audio_line)
    for tag in any_tags:
        if _is_there_one_space_before_substring(purged_line, tag):
            tag = SPACE + tag
        purged_line = purged_line.replace(tag, '')
    # Remove source and it is potential delimiter
    maybe_source = try_extract_web_url(audio_line)
    if maybe_source is not None:
        source_start_index = purged_line.find(maybe_source)
        source_end_index = source_start_index + len(maybe_source)
        # Try to remove delimiting source characters
        previous_source_char_index = max(0, source_start_index - 1)
        if purged_line[previous_source_char_index] != EXPECTED_SOURCE_SEPARATION:
            source_start_index = previous_source_char_index
        next_source_char_index = min(source_end_index + 1, len(purged_line) - 1)
        if purged_line[next_source_char_index] != EXPECTED_SOURCE_SEPARATION:
            source_end_index = next_source_char_index
        source_string_with_separator = purged_line[source_start_index:source_end_index+1]
        if _is_there_one_space_before_substring(purged_line, source_string_with_separator):
            source_string_with_separator = SPACE + source_string_with_separator
        purged_line = purged_line.replace(source_string_with_separator, '')
    return purged_line.strip()

def _playlist_line_to_audio_metadata(line: str) -> AudioMetadata:
    """Extract the metadata from the line"""
    line = remove_carriage_return(line)
    maybe_web_source: str | None = try_extract_web_url(line)
    any_tags: List[str] = try_extract_tags(line)
    title = remove_metadata(line)
    author = ''     # TODO: try to parse the author in the title of the audio
    return AudioMetadata(
        name=title,
        author=author,
        source=maybe_web_source,
        tags=any_tags
    )

def parse_plain_text_playlist_file(playlist_file_absolute_path: str, user_interface: Interface) -> List[AudioMetadata]:
    """Parse the plain text playlist file into a list of audios
        @param playlist_file_absolute_path: str the file path to the plain text file
        @param user_interface: Interface
        @return List[AudioMetadata]: the audios' informations
    """
    user_interface.request_output_to_user("Info: parsing playlist file.")
    audio_data = []
    with open(playlist_file_absolute_path, "rt", encoding=TEXT_ENCODING) as playlist_file:
        lines = playlist_file.readlines()
        for line in lines:
            audio_data.append(_playlist_line_to_audio_metadata(line))
    return audio_data
