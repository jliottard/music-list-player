''' Message levels to dispaly to the user '''

import enum

class MessagePriority(enum.IntEnum):
    ''' Enum class for interfacing priority order of messages '''
    INFO = 3
    LYRICS = 2
    WARNING = 1
    ERROR = 0

