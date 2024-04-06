from typing import List

from lyrics.lyrics_displayer import LyricsDisplayer

def request_lyrics(args: List[str], displayer: LyricsDisplayer):
    """ Handle the arguments to show or hide lyrics
    @param: args: List[str]: first element must be Command.Lyric, the second element is either 'on' 
     or 'off'
    @param: displayer: LyricsDisplayer: the current displayer that displays the audios' lyrics
    """
    if len(args) == 1:
        displayer.set_lyrics(False) # reset in case the lyrics are already displayed
        displayer.set_lyrics(True)
    elif len(args) == 2:
        displayer.set_lyrics(args[1] == 'on')
