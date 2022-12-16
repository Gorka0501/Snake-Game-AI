import pygame as pg
import numpy as np
from SnakeGame.Fruit import Fruit

from SnakeGame.Snake import Body, Snake

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
RED_PALE = (250, 200, 200)
DARK_RED_PALE = (150, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
GREEN_PALE = (200, 250, 200)
DARK_GREEN_PALE = (100, 150, 100)
BLUE = (0, 0, 255)
BLUE_PALE = (200, 200, 255)
DARK_BLUE = (100, 100, 150)
ORANGE = (255, 165, 0)


def draw(
    screen: pg.surface.Surface,
    snake: Snake,
    fruits: list[Fruit],
    table_size: tuple[int, int],
) -> None:

    pg.draw.rect(
        screen, (0, 0, 0), pg.Rect(0, 0, screen.get_width(), screen.get_height())
    )
    bodies = snake.get_bodies()
    for body in bodies:
        x_pos_body, y_pos_body = body.get_pos()
        draw_body(screen, x_pos_body, y_pos_body, table_size)

    x_pos_head, y_pos_head = snake.get_head().get_pos()
    draw_head(screen, x_pos_head, y_pos_head, table_size)

    for fruit in fruits:
        x_pos_fruit, y_pos_fruit = fruit.get_pos()
        draw_fruit(screen, x_pos_fruit, y_pos_fruit, table_size)


def draw_head(
    screen: pg.surface.Surface,
    x_pos_table: int,
    y_pos_table: int,
    table_size: tuple[int, int],
):
    width = screen.get_width() / table_size[0]
    height = screen.get_height() / table_size[1]
    x_pos_screen = x_pos_table * width
    y_pos_screen = y_pos_table * height
    pg.draw.rect(screen, ORANGE, pg.Rect(x_pos_screen, y_pos_screen, width, height))


def draw_body(
    screen: pg.surface.Surface,
    x_pos_table: int,
    y_pos_table: int,
    table_size: tuple[int, int],
):
    width = screen.get_width() / table_size[0]
    height = screen.get_height() / table_size[1]
    x_pos_screen = x_pos_table * width
    y_pos_screen = y_pos_table * height
    pg.draw.rect(screen, DARK_RED, pg.Rect(x_pos_screen, y_pos_screen, width, height))


def draw_fruit(
    screen: pg.surface.Surface,
    x_pos_table: int,
    y_pos_table: int,
    table_size: tuple[int, int],
):
    width = screen.get_width() / table_size[0]
    height = screen.get_height() / table_size[1]
    x_pos_screen = x_pos_table * width
    y_pos_screen = y_pos_table * height
    pg.draw.rect(screen, GREEN_PALE, pg.Rect(x_pos_screen, y_pos_screen, width, height))
