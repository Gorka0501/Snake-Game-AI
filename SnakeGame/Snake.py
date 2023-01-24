import numpy as np

from SnakeGame.Movements import Movements


class Head:

    """
    Represents the Head of the Snake, in the table is represented by a 1.

    Args:
        __x_pos (int): Position of the head on the x axis.
        __y_pos (int): Position of the head on the y axis.
    """

    __x_pos: int = 0
    __y_pos: int = 0

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the Head class.

        Args:
            x (int): Initial position of the head on the x axis.
            y (int): Initial position of the head on the y axis.
        """
        self.__x_pos = x
        self.__y_pos = y

    def move_north(self) -> None:
        self.__y_pos -= 1

    def move_south(self) -> None:
        self.__y_pos += 1

    def move_west(self) -> None:
        self.__x_pos += 1

    def move_east(self) -> None:
        self.__x_pos -= 1

    def get_pos(self) -> tuple[int, int]:
        return self.__x_pos, self.__y_pos


class Body:

    """
    Represents a part of the Body of the Snake, in the table is represented by a 2.

    Args:
        __x_pos (int): Position of this Body part on the x axis.
        __y_pos (int): Position of this Body part on the y axis.
    """

    __x_pos: int = 0
    __y_pos: int = 0

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the Body class.

        Arg:
            x (int): Initial position of the head on the x axis.
            y (int): Initial position of the head on the y axis.
        """
        self.__x_pos = x
        self.__y_pos = y

    def move(self, x: int, y: int) -> None:
        self.__x_pos = x
        self.__y_pos = y

    def get_pos(self) -> tuple[int, int]:
        return self.__x_pos, self.__y_pos


class Snake:
    """
    Represents the Snake and his parts (Head and Bodies).

    Args:
        __length (int): Length of the Snake (Head + number of Bodies)
        __head (Head): Head of the Snake
        __bodies (list[Body]): All the Body parts of the Snake
        __direction (Movements): Direction the Snake is heading.
    """

    __length: int = 1
    __head: Head
    __bodies: list[Body]
    __direction: Movements

    def __init__(
        self, table_width: int, table_height: int, body_length: int = 0
    ) -> None:
        head_x = np.random.choice(range(table_width))
        head_y = np.random.choice(range(table_height))
        self.__head = Head(head_x, head_y)
        self.__bodies = []
        self.__direction = Movements.STOP

    def get_length(self) -> int:
        return self.__length

    def get_head(self) -> Head:
        return self.__head

    def get_bodies(self) -> list[Body]:
        return self.__bodies

    def get_direction(self) -> Movements:
        return self.__direction

    def change_direction(self, mov: Movements) -> None:
        if (
            (mov == Movements.NORTH and not (self.__direction == Movements.SOUTH))
            or (mov == Movements.SOUTH and not (self.__direction == Movements.NORTH))
            or (mov == Movements.WEST and not (self.__direction == Movements.EAST))
            or (mov == Movements.EAST and not (self.__direction == Movements.WEST))
            or self.__length == 1
        ):
            self.__direction = mov

    def increase(self, head_pos: tuple[int, int]) -> None:
        self.__length += 1
        if len(self.__bodies) == 0:
            x_body, y_body = head_pos
        else:
            last_body = self.__bodies[len(self.__bodies) - 1]
            x_body, y_body = last_body.get_pos()
        self.__bodies.append(Body(x_body, y_body))

    def move_bodies(self, head_pos: tuple[int, int]) -> None:
        body_aux_pos = head_pos
        for body in self.__bodies:
            body_aux_pos2 = body.get_pos()
            body.move(*body_aux_pos)
            body_aux_pos = body_aux_pos2

    def move_head(self) -> None:
        match self.__direction:
            case Movements.NORTH:
                self.__head.move_north()
            case Movements.SOUTH:
                self.__head.move_south()
            case Movements.WEST:
                self.__head.move_west()
            case Movements.EAST:
                self.__head.move_east()
            case Movements.STOP:
                pass

    def update(self) -> None:
        self.move_bodies(self.get_head().get_pos())
        self.move_head()

    def get_occupied(self) -> list[tuple[int, int]]:
        occupied = []
        occupied.append(self.__head.get_pos())
        for body in self.__bodies:
            if not (body.get_pos() in occupied):
                occupied.append(body.get_pos())
        return occupied
