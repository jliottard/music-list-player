from audio.audio_player import AudioPlayer

def request_volume(args: list, player: AudioPlayer):
    ''' Change or show volume information '''
    if len(args) == 1:
        print(f"Audio's volume is {player.get_volume()}%.")
    elif len(args) == 2:
        volume_integer = 0
        try:
            volume_integer = int(args[1])
        except ValueError:
            print(f"Error: the second argument \"{args[1]}\" is not an integer. So, the audio's volume cannot be changed.")
            return
        player.set_volume(volume_integer)
        print("Updating audio's volume")
