import os
import platform
from threading import Lock

from audio.audio import Audio
from audio.audio_player import AudioPlayer

class Interface:
    """Class responsible to controlling input and ouput from and to user for multhreading access"""

    def __init__(self):
        self.stin_lock = Lock()
        self.stout_lock = Lock()

    @staticmethod
    def _clean_terminal() -> None:
        """Clean the terminal"""
        match platform.system():
            case "Windows":
                os.system('cls')
            case "Linux":
                os.system('clear')
            case _:
                os.system('clear')

    @staticmethod
    def status_information_str(player: AudioPlayer) -> str:
        """Return the player basics information such as playing song and upcoming song
        @param palyer: AudioPlayer
        """
        status_info = ""
        if player.is_playing():
            maybe_current_song: Audio = player.get_playing_audio()
            current_song_name = ""
            if maybe_current_song is None:
                current_song_name = "unknown"
            else:
                current_song_name = maybe_current_song.name
            status_info = f"Currently playing: {current_song_name}."
            maybe_next_audio: Audio = player.get_next_audio()
            if maybe_next_audio is not None:
                status_info +=  f"\nNext song: {maybe_next_audio.name}."
        else:
            status_info = "No audio is playing."
        return status_info

    def book_user_input(self):
        """Acquire the lock for accessing user's input"""
        self.stin_lock.acquire()

    def free_user_input(self):
        """Acquire the lock for accessing user's input"""
        self.stin_lock.release()

    def receive_input_from_user(self) -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is already booked
        @return: str the user's input
        """
        return input()

    def request_input_from_user(self) -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is not booked
        @return: str the user's input
        """
        self.book_user_input()
        user_input = self.receive_input_from_user()
        self.free_user_input()
        return user_input

    def request_output_to_user(self, output: str):
        """Place to interface's next requested action to user_interface.request_output_to_user the <output>
        @param output: str the message to user_interface.request_output_to_user to the user
        """
        with self.stout_lock:
            print(output)

    def update_app_display(self, player: AudioPlayer):
        """Refresh the terminal to display current status information
        @param player: AudioPlayer
        """
        with self.stout_lock:
            self._clean_terminal()
        self.request_output_to_user(Interface.status_information_str(player))
