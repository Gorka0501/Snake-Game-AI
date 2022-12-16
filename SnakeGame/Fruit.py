import numpy as np

from SnakeGame.Snake import Snake


class Fruit:
    __x_pos: int = 0
    __y_pos: int = 0
    __is_eaten: bool = False

    def __init__(
        self, table_width: int, table_height: int, occupied: list[tuple[int, int]]
    ) -> None:
        self.set_position(table_width, table_height, occupied)

    def set_position(
        self, table_width: int, table_height: int, occupied: list[tuple[int, int]]
    ) -> None:
        x_pos = np.random.choice(range(table_height))
        y_pos = np.random.choice(range(table_width))
        while (x_pos, y_pos) in occupied:
            x_pos = np.random.choice(range(table_height))
            y_pos = np.random.choice(range(table_width))
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__is_eaten = False

    def get_pos(self) -> tuple[int, int]:
        return self.__x_pos, self.__y_pos

    def eaten(self) -> None:
        self.__is_eaten = True

    def get_is_eaten(self) -> bool:
        return self.__is_eaten
