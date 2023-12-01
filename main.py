from download import get_youtube_url, download_audio
from playsound import playsound
from enum import Enum

def play_audio(audio_filepath: str) -> None:
    print(f"Currently playing: {audio_filepath}")
    playsound(audio_filepath)

class Audio:
    def __init__(self, name: str, filepath: str):
        self.name = name
        self.filepath = filepath

class Playlist:
    def __init__(self):
        self.audios: list[Audio] = []
        self.current_music_index = 0

class Command(Enum):
    HELP = "help"
    QUIT = "quit"
    IMPORT = "import"
    PLAY = "play"
    LIST = "list"

if __name__ == "__main__":
    print("Welcome to music list player! Please enter a command (type: \"help\" for help).")
    playlist = Playlist()
    while True:
        user_input = input()
        # todo: pre-parser for security?
        #command = parse_command(user_input)
        command = user_input
        if command == Command.QUIT.value:
            print("Goodbye!")
            break
        elif command == Command.HELP.value:
            commands = list(Command)
            print(f"The commands available are : {commands}")
        elif command == Command.IMPORT.value:
            # todo: add custom input file
            playlist_filepath = "playlist.txt"
            with open(playlist_filepath, "rt") as musics_list_file:
                musics_list = musics_list_file.readlines()
            print(f"Importing audios from \"{playlist_filepath}\".")
            musics_list_file.close()
            audio_paths = []
            for music in musics_list:
                # Search music video
                music_url: str = get_youtube_url(music)
                # Download audio
                playlist.audios.append(
                    Audio(
                        name=music,
                        filepath=download_audio(music_url)
                    )
                )
        elif command == Command.PLAY.value:
            # Play current music audio
            current_audio = playlist.audios[playlist.current_music_index]
            play_audio(current_audio.filepath)
            print(f"Playing {current_audio.name}")
        elif command == Command.LIST.value:
            print("Music list:")
            for index, audio in enumerate(playlist.audios):
                if index == playlist.current_music_index:
                    print(f"- {audio.name} (currently playing)")
                else:
                    print(f"- {audio.name}")

