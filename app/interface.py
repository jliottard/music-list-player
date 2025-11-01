import os
import platform
from threading import Lock

from app.message_priority import MessagePriority
from audio.audio import Audio
from audio.audio_player import AudioPlayer

class Interface:
    """Class responsible for controlling input and ouput from and to user for multhreading access"""

    def __init__(self):
        self.stdin_lock = Lock()
        self.stdout_lock = Lock()
        self.messages_by_priority = [ [] for priority in MessagePriority ]
        self.priority_locks = { priority:Lock() for priority in MessagePriority }
        self.msg_prio_mutenesses = { priority:False for priority in MessagePriority }

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
    def playing_audio_status(player: AudioPlayer) -> str:
        """ Return the status for the current playing audio
        @param player: AudioPlayer
        """
        maybe_current_song: Audio = player.get_playing_audio()
        current_song_name = ""
        if maybe_current_song is None:
            current_song_name = "unknown"
        else:
            current_song_name = maybe_current_song.name_without_extension
        maybe_audio_time_progess_in_sec: float = player.get_audio_progress_time_in_sec()
        maybe_audio_duration_in_sec: float = player.get_playing_audio_duration_in_sec()
        status_info = f"{current_song_name}"
        progress_string = ""
        if maybe_audio_time_progess_in_sec is None:
            progress_string = "?"
        else:
            progress_string = f"{maybe_audio_time_progess_in_sec:.2f}s"
        duration_string = ""
        if maybe_audio_duration_in_sec is None:
            duration_string = "?"
        else:
            duration_string = f"{maybe_audio_duration_in_sec:.2f}s"
        status_info += f" ({progress_string} / {duration_string})"
        return status_info

    @staticmethod
    def status_information_str(player: AudioPlayer) -> str:
        """Return the player basics information such as playing song and upcoming song
        @param player: AudioPlayer
        """
        status_info = ""
        if player.is_playing():
            playing_audio_info: str = Interface.playing_audio_status(player)
            status_info = "Info:\n"
            status_info += f" - Currently playing: {playing_audio_info}."
            maybe_next_audio: Audio = player.get_next_audio()
            if maybe_next_audio is not None:
                status_info +=  f"\n - Next song: \"{maybe_next_audio.name_without_extension}\"."
        else:
            status_info = "Info: no audio is playing."
        return status_info

    @staticmethod
    def receive_input_from_user() -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is already booked
        @return: str the user's input
        """
        return input()

    def book_user_input(self):
        """Acquire the lock for accessing user's input"""
        self.stdin_lock.acquire()

    def free_user_input(self):
        """Acquire the lock for accessing user's input"""
        self.stdin_lock.release()

    def request_input_from_user(self) -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is not booked
        @return: str the user's input
        """
        self.book_user_input()
        user_input = self.receive_input_from_user()
        self.free_user_input()
        return user_input

    def request_output_to_user(self, output: str, priority: MessagePriority):
        """Place to interface's next requested action to send the
         <output>
        @param output: str the message to send to the user
        @param priority: MessagePriority
        """
        # Store the message by priority
        with self.priority_locks[priority]:
            self.messages_by_priority[priority].append(output)
        # Display messages by priority and ignore messages with muted priority
        with self.stdout_lock:
            for priority in MessagePriority:
                with self.priority_locks[priority]:
                    if len(self.messages_by_priority[priority]) == 0:
                        continue
                    message = self.messages_by_priority[priority].pop(0)
                    if self.msg_prio_mutenesses[priority]:
                        # we discard messages in a muted priority/level to not display them later when they would not be relevant anymore.
                        continue
                    print(message)

    def update_app_display(self, player: AudioPlayer):
        """Refresh the terminal to display current status information
        @param player: AudioPlayer
        """
        with self.stdout_lock:
            self._clean_terminal()
        self.request_output_to_user(Interface.status_information_str(player), MessagePriority.INFO)

    def mute_message(self, priority: MessagePriority):
        ''' Mute the messages from the given priority '''
        with self.priority_locks[priority]:
            self.msg_prio_mutenesses[priority] = True

    def unmute_message(self, priority: MessagePriority):
        ''' Unmute the messages from the given priority '''
        with self.priority_locks[priority]:
            self.msg_prio_mutenesses[priority] = False

    def muteness_status(self):
        ''' Display which priorities are muted or not '''
        muteness_status: str = "Muteness status:"
        for priority in MessagePriority:
            status = "NOT muted."
            if self.msg_prio_mutenesses[priority]:
                status = "muted."
            muteness_status += "\n"
            muteness_status += f"\tThe {priority} priority is {status}"

        return muteness_status