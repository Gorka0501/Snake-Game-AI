import re
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

    x_width: int = 0
    y_height: int = 0
    snake: Snake
    matrix: np.ndarray
    fruits: list[Fruit] = []

    def __init__(self, x: int, y: int) -> None:
        self.x_width = x
        self.y_height = y
        self.matrix = np.zeros(shape=(x, y), dtype=np.int8)
        self.snake = Snake(self.x_width, self.y_height)
        self.fruits.append(Fruit(self.x_width, self.y_height, self.get_occupied()))
        self.update_matrix()

    def get_occupied(self) -> list[tuple[int, int]]:
        occupied = []
        occupied.extend(self.snake.get_occupied())
        for fruit in self.fruits:
            if not fruit.get_pos() in occupied:
                occupied.append(fruit.get_pos())
        return occupied

    def get_matrix(self) -> np.ndarray:
        return self.matrix

    def update_matrix(self) -> None:
        self.matrix = np.zeros(shape=(self.x_width, self.y_height), dtype=np.int8)

        snake_head_x_pos, snake_head_y_pos = self.snake.get_head().get_pos()
        if not self.matrix[snake_head_y_pos][snake_head_x_pos] == 2:
            self.matrix[snake_head_y_pos][snake_head_x_pos] = 1

        for body_number, body in enumerate(self.snake.get_bodies()):
            body_x_pos, body_y_pos = body.get_pos()
            if not (
                body_number == len(self.snake.get_bodies()) - 1
                and self.matrix[body_y_pos][body_x_pos] == 1
            ):
                self.matrix[body_y_pos][body_x_pos] = 2

        for fruit in self.fruits:
            fruit_x_pos, fruit_y_pos = fruit.get_pos()
            self.matrix[fruit_y_pos][fruit_x_pos] = 3

    def snake_out_of_bounds(self, head_pos: tuple[int, int]) -> bool:

        head_x_pos, head_y_pos = head_pos
        if (
            head_x_pos < 0
            or head_x_pos > self.x_width - 1
            or head_y_pos < 0
            or head_y_pos > self.y_height - 1
        ):
            return True

        return False

    def ate_tail(self, head_pos: tuple[int, int]) -> bool:
        if len(self.snake.get_bodies()) > 1 and head_pos in [
            body.get_pos() for body in self.snake.get_bodies()
        ]:
            return True

        return False

    def absolute_win(self) -> bool:
        if len(self.snake.get_occupied()) == self.x_width * self.y_height:
            return True
        return False

    def update(self) -> tuple[bool, int]:
        """Updates the table an all of the objects inside.

        Returns:
            tuple[bool, int]: A Tuple with the a Boolean representing to end the Game and a Integer representing why it has/hasn't ended.
        """

        self.snake.update()
        head_pos = self.snake.get_head().get_pos()
        if self.snake_out_of_bounds(head_pos):
            return True, 1

        if self.ate_tail(head_pos):
            self.update_matrix()
            return True, 2

        if self.absolute_win():
            self.update_matrix()
            return True, 0

        for fruit_idx, fruit in enumerate(self.fruits):
            if fruit.get_pos() == head_pos:
                self.snake.increase(head_pos)

                del self.fruits[fruit_idx]
                self.fruits.append(
                    Fruit(self.x_width, self.y_height, self.get_occupied())
                )

            self.update_matrix()
            return False, 1

        self.update_matrix()
        return False, 0
