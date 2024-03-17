from app.interface import Interface
from audio.audio_player import AudioPlayer

def request_volume(args: list, player: AudioPlayer, user_interface: Interface):
    """Change or show volume information
    @param args: List[Command, str..]
    @param player: AudioPlayer
    @param user_interface: Interface
    """
    if len(args) == 1:
        user_interface.request_output_to_user(f"Audio's volume is {player.get_volume()}%.")
    elif len(args) == 2:
        volume_integer = 0
        try:
            volume_integer = int(args[1])
        except ValueError:
            user_interface.request_output_to_user(f"Error: the second argument \"{args[1]}\" is not an integer. So, the audio's volume cannot be changed.")
            return
        player.set_volume(volume_integer)
        user_interface.request_output_to_user("Updating audio's volume")
