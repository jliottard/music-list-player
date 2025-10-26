
from audio.audio_player import AudioPlayer
from app.interface import Interface
from app.message_priority import MessagePriority

class InterfaceMock(Interface):
    """Mock class responsible for controlling input and ouput from and to user for multhreading access"""

    def __init__(self):
        pass

    @staticmethod
    def _clean_terminal() -> None:
        """Clean the terminal"""
        pass

    @staticmethod
    def playing_audio_status(player: AudioPlayer) -> str:
        """ Return the status for the current playing audio
        @param player: AudioPlayer
        """
        pass

    @staticmethod
    def status_information_str(player: AudioPlayer) -> str:
        """Return the player basics information such as playing song and upcoming song
        @param player: AudioPlayer
        """
        pass

    @staticmethod
    def receive_input_from_user() -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is already booked
        @return: str the user's input
        """
        pass

    def book_user_input(self):
        """Acquire the lock for accessing user's input"""
        pass
    
    def free_user_input(self):
        """Acquire the lock for accessing user's input"""
        pass

    def request_input_from_user(self) -> str:
        """Place to interface's next requested action to get the user's <input>
        Assume the user's input is not booked
        @return: str the user's input
        """
        pass

    def request_output_to_user(self, output: str, priority: MessagePriority):
        """Place to interface's next requested action to user_interface.request_output_to_user the <output>
        @param output: str the message to user_interface.request_output_to_user to the user
        """
        pass

    def update_app_display(self, player: AudioPlayer):
        """Refresh the terminal to display current status information
        @param player: AudioPlayer
        """
        pass
    
    def mute_message(self, priority: MessagePriority):
        ''' Mute the messages from the given priority '''
        pass

    def unmute_message(self, priority: MessagePriority):
        ''' Unmute the messages from the given priority '''
        pass
