from typing import List

from lyrics.lyrics_displayer import LyricsDisplayer
    
def request_lyrics(args: List[str], displayer: LyricsDisplayer):
    ''' Handle the arguments to show or hide lyrics
    @param: args: List[str]: first element must be Command.Lyric, the second element is either 'on' or 'off'
    @param: displayer: LyricsDisplayer: the current displayer that displays the audios' lyrics
    '''
    if len(args) < 2:
        return
    displayer.set_lyrics(args[1] == 'on')
