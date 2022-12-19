from math import ceil
import pygame as pg
from SnakeGame.Fruit import Fruit
from SnakeGame.GameData import GameData

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


class GameScreen:
    __x_width: int
    __y_height: int
    __screen: pg.surface.Surface
    __table_x_squares: int
    __table_y_squares: int

    def __init__(self, x_squares: int, y_squares: int) -> None:
        self.__x_width = x_squares + 1
        self.__y_height = y_squares + 4
        self.__table_x_squares = x_squares
        self.__table_y_squares = y_squares
        self.create_display()

    def create_display(self) -> None:
        self.__screen = pg.display.set_mode(
            (
                self.__x_width * 50,
                self.__y_height * 50,
            )
        )

    def draw(self, snake: Snake, fruits: list[Fruit], game_data: GameData) -> None:

        play_surface_partition = 4 / 5
        game_data_partition = 1 - play_surface_partition
        self.draw_data(game_data, game_data_partition)
        self.draw_play_surface(snake, fruits, play_surface_partition)

    def draw_data(self, game_data: GameData, game_data_partition: float) -> None:
        screen = self.__screen
        data_surface = screen.subsurface(
            pg.Rect(
                0,
                0,
                screen.get_width(),
                screen.get_height() * game_data_partition,
            )
        )
        data_surface.fill(BLACK)
        data_font = pg.font.SysFont("comicsansms", round(data_surface.get_height() / 2))
        score_text = data_font.render(str(game_data.score), True, WHITE)
        turns_without_eat_text = data_font.render(
            str(game_data.turns_without_eat), True, WHITE
        )
        data_surface.blit(
            score_text,
            (
                data_surface.get_width() // 4 - score_text.get_width() // 2,
                data_surface.get_height() // 10,
            ),
        )
        data_surface.blit(
            turns_without_eat_text,
            (
                data_surface.get_width() // 4 * 3
                - turns_without_eat_text.get_width() // 2,
                data_surface.get_height() // 10,
            ),
        )
        print(
            data_surface.get_height() // 10,
            data_font.get_height(),
            round(data_surface.get_height() / 10 * 8),
        )

    def draw_play_surface(
        self, snake: Snake, fruits: list[Fruit], play_surface_partition: float
    ) -> None:

        screen = self.__screen
        play_surface = screen.subsurface(
            pg.Rect(
                0,
                screen.get_height() * (1 - play_surface_partition),
                screen.get_width(),
                screen.get_height() * play_surface_partition,
            )
        )

        square_width = play_surface.get_width() / self.__x_width
        square_height = play_surface.get_height() / self.__y_height
        table_surface = play_surface.subsurface(
            pg.Rect(
                square_width / 2,
                square_height / 2,
                play_surface.get_width() - square_width,
                play_surface.get_height() - square_height,
            )
        )

        self.draw_table(table_surface, snake, fruits)
        border_width = ceil(max(square_width / 2, square_height / 2))
        self.draw_play_border(play_surface, border_width)

    def draw_play_border(
        self, play_surface: pg.surface.Surface, border_width: int
    ) -> None:
        pg.draw.rect(
            play_surface,
            DARK_GREEN,
            pg.Rect(
                0,
                0,
                play_surface.get_width(),
                play_surface.get_height(),
            ),
            width=border_width,
        )

    def draw_table(
        self, table_surface: pg.surface.Surface, snake: Snake, fruits: list[Fruit]
    ) -> None:

        pg.draw.rect(
            table_surface,
            (0, 0, 0),
            pg.Rect(0, 0, table_surface.get_width(), table_surface.get_height()),
        )
        bodies = snake.get_bodies()
        for body in bodies:
            x_pos_body, y_pos_body = body.get_pos()
            self.draw_body(table_surface, x_pos_body, y_pos_body)

        x_pos_head, y_pos_head = snake.get_head().get_pos()
        self.draw_head(table_surface, x_pos_head, y_pos_head)

        for fruit in fruits:
            x_pos_fruit, y_pos_fruit = fruit.get_pos()
            self.draw_fruit(table_surface, x_pos_fruit, y_pos_fruit)

    def draw_head(
        self, table_surface: pg.surface.Surface, x_pos_table: int, y_pos_table: int
    ) -> None:
        width = table_surface.get_width() / self.__table_x_squares
        height = table_surface.get_height() / self.__table_y_squares
        x_pos_table_surface = x_pos_table * width
        y_pos_table_surface = y_pos_table * height
        pg.draw.rect(
            table_surface,
            ORANGE,
            pg.Rect(x_pos_table_surface, y_pos_table_surface, width, height),
        )

    def draw_body(
        self, table_surface: pg.surface.Surface, x_pos_table: int, y_pos_table: int
    ) -> None:
        width = table_surface.get_width() / self.__table_x_squares
        height = table_surface.get_height() / self.__table_y_squares
        x_pos_table_surface = x_pos_table * width
        y_pos_table_surface = y_pos_table * height
        pg.draw.rect(
            table_surface,
            DARK_RED,
            pg.Rect(x_pos_table_surface, y_pos_table_surface, width, height),
        )

    def draw_fruit(
        self, table_surface: pg.surface.Surface, x_pos_table: int, y_pos_table: int
    ) -> None:
        width = table_surface.get_width() / self.__table_x_squares
        height = table_surface.get_height() / self.__table_y_squares
        x_pos_table_surface = x_pos_table * width
        y_pos_table_surface = y_pos_table * height
        pg.draw.rect(
            table_surface,
            GREEN_PALE,
            pg.Rect(x_pos_table_surface, y_pos_table_surface, width, height),
        )
