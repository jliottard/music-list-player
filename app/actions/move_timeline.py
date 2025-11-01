''' "move" command functionnality '''

from audio.audio_player import AudioPlayer

def request_move(args: list, player: AudioPlayer) -> None:
    """Change the playing audio played moment"""
    if len(args) == 2:
        time: int = int(args[1])
        player.set_current_audio_time(time)
