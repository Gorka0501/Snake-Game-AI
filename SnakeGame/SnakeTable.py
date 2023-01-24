from dataclasses import field
import numpy as np
from SnakeGame.Fruit import Fruit
from SnakeGame.Snake import Snake


"""
0 Empty tile
1 Snake Head tile
2 Snake Body tile
3 Fruit tile
"""


class SnakeTable:

    __x_squares: int = 0
    __y_squares: int = 0
    __snake: Snake
    __fruits: list[Fruit]

    def __init__(self, x: int, y: int) -> None:
        self.__x_squares = x
        self.__y_squares = y
        self.__snake = Snake(self.__x_squares, self.__y_squares)
        self.__fruits = []
        self.__fruits.append(
            Fruit(self.__x_squares, self.__y_squares, self.get_occupied())
        )

    def get_occupied(self) -> list[tuple[int, int]]:
        occupied = []
        occupied.extend(self.__snake.get_occupied())
        for fruit in self.__fruits:
            if not fruit.get_pos() in occupied:
                occupied.append(fruit.get_pos())
        return occupied

    def get_snake(self) -> Snake:
        return self.__snake

    def get_fruits(self) -> list[Fruit]:
        return self.__fruits

    def snake_out_of_bounds(self, head_pos: tuple[int, int]) -> bool:

        head_x_pos, head_y_pos = head_pos
        if (
            head_x_pos < 0
            or head_x_pos > self.__x_squares - 1
            or head_y_pos < 0
            or head_y_pos > self.__y_squares - 1
        ):
            return True

        return False

    def ate_tail(self, head_pos: tuple[int, int]) -> bool:
        if len(self.__snake.get_bodies()) > 1 and head_pos in [
            body.get_pos() for body in self.__snake.get_bodies()
        ]:
            return True

        return False

    def absolute_win(self) -> bool:
        if len(self.__snake.get_occupied()) == self.__x_squares * self.__y_squares:
            return True
        return False

    def update(self) -> tuple[bool, int]:
        """Updates the table an all of the objects inside.

        Returns:
            tuple[bool, int]: A Tuple with the a Boolean representing to end the Game and a Integer representing why it has/hasn't ended.
        """

        self.__snake.update()
        head_pos = self.__snake.get_head().get_pos()
        if self.snake_out_of_bounds(head_pos):
            return True, 0

        if self.ate_tail(head_pos):
            return True, 2

        if self.absolute_win():
            return True, 1
        for fruit_idx, fruit in enumerate(self.__fruits):
            if fruit.get_pos() == head_pos:
                self.__snake.increase(head_pos)

                del self.__fruits[fruit_idx]
                self.__fruits.append(
                    Fruit(self.__x_squares, self.__y_squares, self.get_occupied())
                )

                return False, 1

        return False, 0
