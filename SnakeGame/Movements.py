from enum import Enum, auto


class Movements(Enum):
    """
    Enum class with the possible movements (NORTH, SOUTH, EAST, WEST, STOP)
    """

    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    STOP = auto()
