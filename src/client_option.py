from enum import IntEnum
from enum import auto

class Option(IntEnum):
    CONNECT = auto()
    QUIT = auto()
    UPLOAD = auto()

    def __str__(self) -> str:
        """ Returns a string which represents the option.
        """

        return self.name.replace('_', ' ').capitalize()
