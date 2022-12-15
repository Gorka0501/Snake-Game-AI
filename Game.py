from enum import Enum, auto
import pygame as pg
import numpy as np

"""
0 Empty tile
1 Snake Head tile
2 Snake Body tile
3 Fruit tile
"""


class Movements(Enum):
    """
    Enum class with the possible movements (NORTH, SOUTH, EAST, WEST, STOP)
    """

    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    STOP = auto()


class Head:

    """
    Represents the Head of the Snake, in the matrix is represented by a 1.

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
    Represents a part of the Body of the Snake, in the matrix is represented by a 2.

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
        __body (list[Body]): All the Body parts of the Snake
        __direction (Movements): Direction the Snake is heading.
    """

    __length: int = 1
    __head: Head
    __body: list[Body]
    __direction: Movements

    def __init__(self, table_matrix: np.ndarray) -> None:
        head_x = np.random.choice(range(len(table_matrix[0]) - 1))
        head_y = np.random.choice(
            range(min(2, len(table_matrix) - 1), len(table_matrix))
        )
        self.__head = Head(head_x, head_y)
        self.__body = []
        self.__direction = Movements.STOP

    def get_length(self) -> int:
        return self.__length

    def get_head(self) -> Head:
        return self.__head

    def get_body(self) -> list[Body]:
        return self.__body

    def change_direction(self, mov: Movements) -> None:
        if (
            (mov == Movements.NORTH and not (self.__direction == Movements.SOUTH))
            or (mov == Movements.SOUTH and not (self.__direction == Movements.NORTH))
            or (mov == Movements.WEST and not (self.__direction == Movements.EAST))
            or (mov == Movements.EAST and not (self.__direction == Movements.WEST))
            or (self.__length == 1)
        ):
            self.__direction = mov

    def increase(self, head_pos: tuple[int, int]) -> None:
        self.__length += 1
        if len(self.__body) == 0:
            x_body, y_body = head_pos
        else:
            last_body = self.__body[len(self.__body) - 1]
            x_body, y_body = last_body.get_pos()
        self.__body.append(Body(x_body, y_body))

    def move_body(self, head_pos: tuple[int, int]) -> None:
        body_aux_pos = head_pos
        for body in self.__body:
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

    def update(self, fruit_pos: tuple[int, int]) -> None:
        pos_head_aux = self.get_head().get_pos()
        self.move_body(pos_head_aux)
        self.move_head()
        if self.__head.get_pos() == fruit_pos:
            self.increase(pos_head_aux)


class Fruit:
    __x_pos: int = 0
    __y_pos: int = 0

    def __init__(self, table_matrix: np.ndarray, head_pos: tuple[int, int]) -> None:
        self.set_position(table_matrix, head_pos)

    def set_position(self, table_matrix: np.ndarray, head_pos: tuple[int, int]) -> None:
        x_pos = np.random.choice(range(len(table_matrix[0])))
        y_pos = np.random.choice(range(len(table_matrix)))
        head_x_pos, head_y_pos = head_pos
        while table_matrix[y_pos][x_pos] != 0 or (
            x_pos == head_x_pos and y_pos == head_y_pos
        ):
            x_pos = np.random.choice(range(len(table_matrix[0])))
            y_pos = np.random.choice(range(len(table_matrix)))
        self.__x_pos = x_pos
        self.__y_pos = y_pos

    def get_pos(self) -> tuple[int, int]:
        return self.__x_pos, self.__y_pos


class Table:

    x_width: int = 0
    y_height: int = 0
    snake: Snake
    matrix: np.ndarray
    fruit: Fruit

    def __init__(self, x: int, y: int) -> None:
        self.x_width = x
        self.y_height = y
        self.matrix = np.zeros(shape=(x, y), dtype=np.int8)
        self.snake = Snake(self.matrix)
        self.fruit = Fruit(self.matrix, self.snake.get_head().get_pos())
        self.update_matrix()

    def get_matrix(self) -> np.ndarray:
        return self.matrix

    def update_matrix(self) -> None:
        self.matrix = np.zeros(shape=(self.x_width, self.y_height), dtype=np.int8)

        snake_head_x_pos, snake_head_y_pos = self.snake.get_head().get_pos()
        self.matrix[snake_head_y_pos][snake_head_x_pos] = 1

        for body in self.snake.get_body():
            body_x_pos, body_y_pos = body.get_pos()
            self.matrix[body_y_pos][body_x_pos] = 2

        fruit_x_pos, fruit_y_pos = self.fruit.get_pos()
        self.matrix[fruit_y_pos][fruit_x_pos] = 3

    def is_end(self, head_pos: tuple[int, int]) -> tuple[bool, int]:

        head_x_pos, head_y_pos = head_pos
        if self.snake.get_length() >= self.x_width * self.y_height:
            return True, 0

        if (
            head_x_pos < 0
            or head_x_pos > self.x_width - 1
            or head_y_pos < 0
            or head_y_pos > self.y_height - 1
        ):
            return True, 1

        if self.matrix[head_y_pos][head_x_pos] == 2:
            return True, 2

        return False, 0

    def update(self) -> tuple[bool, int]:
        """Updates the table an all of the objects inside.

        Returns:
            tuple[bool, int]: A Tuple with the a Boolean representing to end the Game and a Integer representing why it has/hasn't ended.
        """
        self.snake.update(self.fruit.get_pos())
        head_x_pos, head_y_pos = self.snake.get_head().get_pos()
        end, why = self.is_end((head_x_pos, head_y_pos))
        if end:
            return end, why
        if self.matrix[head_y_pos][head_x_pos] == 3:
            self.fruit.set_position(self.matrix, self.snake.get_head().get_pos())
        self.update_matrix()

        return end, why


def main():
    pg.init()

    pg.mouse.set_visible(False)

    display_width = 800
    display_height = 800
    screen = pg.display.set_mode((display_width, display_height), False)

    clock = pg.time.Clock()

    table = Table(3, 3)

    end = False
    while not end:
        clock.tick(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            table.snake.change_direction(Movements.NORTH)
        if keys[pg.K_s]:
            table.snake.change_direction(Movements.SOUTH)
        if keys[pg.K_d]:
            table.snake.change_direction(Movements.WEST)
        if keys[pg.K_a]:
            table.snake.change_direction(Movements.EAST)
        end, why = table.update()
        print(table.get_matrix(), table.snake.get_length())
        if end:
            match why:
                case 0:
                    print(f"YOU WIN")
                case 1:
                    print(f"YOU LOSE. \n You crashed against a wall")
                case 2:
                    print(f"YOU LOSE. \n You ate your own tail")
            pg.quit()


np.set_printoptions(threshold=np.inf)  # type:ignore
main()
