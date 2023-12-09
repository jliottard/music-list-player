#!/usr/bin/python3
from download import get_youtube_url, download_audio
from audio_player import Audio, Playlist, AudioPlayer
from command import Command

if __name__ == "__main__":
    playlist = Playlist()
    player = AudioPlayer(playlist)
    print("Welcome to music list player! Please enter a command (type: \"help\" for help).")
    while True:
        user_input = input()
        # todo: pre-parser for security?
        #command = parse_command(user_input)
        command = user_input
        if command == Command.QUIT.value:
            print("Goodbye!")
            break
        elif command == Command.HELP.value:
            print(f"The commands available are :") 
            for command in list(Command):
                help = command.help()
                print(f"- {command.value}\t{help}")
        elif command == Command.IMPORT.value:
            # todo: add custom input file
            playlist_filepath = "playlist.txt"
            with open(playlist_filepath, "rt") as musics_list_file:
                musics_list = musics_list_file.readlines()
            print(f"Importing audios from \"{playlist_filepath}\".")
            musics_list_file.close()
            audio_paths = []
            for music in musics_list:
                music_url: str = get_youtube_url(music)
                playlist.audios.append(
                    Audio(
                        name=music,
                        filepath=download_audio(music_url)
                    )
                )
            del(player)
            player = AudioPlayer(playlist)
        elif command == Command.LIST.value:
            print("Music list:")
            for index, audio in enumerate(playlist.audios):
                if index == playlist.current_audio_index:
                    print(f"- {audio.name} (currently playing)")
                else:
                    print(f"- {audio.name}")
        elif command == Command.PLAY.value:
            player.play()
            print(f"Playing {player.playlist.current_audio().name}")
        elif command == Command.NEXT.value:
            player.next()
            print(f"Skiping to next audio:{player.playlist.current_audio().name}")
        elif command == Command.STOP.value:
            player.stop()
            print("Stopping the audio")
        elif command == Command.PAUSE.value:
            player.pause()
            if player.is_playing():
                print("Pausing the audio")
            else:
                print("Resuming the audio")
        else:
            print("Command unknown")

