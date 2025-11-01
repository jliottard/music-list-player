''' Priorities for the message displayed to the user '''

import enum

class MessagePriority(enum.IntEnum):
    ''' Enum class for interfacing priority order of messages '''
    INFO = 3
    LYRICS = 2
    WARNING = 1
    ERROR = 0

    def __str__(self) -> str:
        match self.value:
            case MessagePriority.INFO:
                return "info"
            case MessagePriority.LYRICS:
                return "lyrics"
            case MessagePriority.WARNING:
                return "warning"
            case MessagePriority.ERROR:
                return "error"
            case _:
                return ""

    @staticmethod
    def from_string(string: str):
        for priority in MessagePriority:
            if string == str(priority):
                return priority
        raise ValueError("Not matching priority.")