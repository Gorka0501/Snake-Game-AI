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
    __square_width: int
    __square_height: int
    __screen: pg.surface.Surface
    __table_x_squares: int
    __table_y_squares: int
    __display_width: int = 900
    __display_height: int = 900

    def __init__(self, x_squares: int, y_squares: int) -> None:

        self.__square_width = self.__display_width // (x_squares + 1)
        self.__square_height = self.__display_height * 8 // 10 // (y_squares + 1)
        square_size = min(self.__square_height, self.__square_width)
        self.__square_width = square_size
        self.__square_height = square_size
        self.__table_x_squares = x_squares
        self.__table_y_squares = y_squares
        self.create_display()

    def create_display(self) -> None:
        self.__screen = pg.display.set_mode(
            (self.__display_width, self.__display_width),
        )

    def draw(self, snake: Snake, fruits: list[Fruit], game_data: GameData) -> None:

        self.draw_data(game_data)
        self.draw_play_surface(snake, fruits)

    def draw_data(self, game_data: GameData) -> None:
        data_height = self.__display_height - (
            self.__square_height * (self.__table_y_squares + 1)
        )
        screen = self.__screen
        data_surface = screen.subsurface(
            pg.Rect(
                0,
                0,
                screen.get_width(),
                data_height,
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

    def draw_play_surface(self, snake: Snake, fruits: list[Fruit]) -> None:

        data_height = self.__display_height - (
            self.__square_height * (self.__table_y_squares + 1)
        )
        screen = self.__screen
        play_surface = screen.subsurface(
            pg.Rect(
                0,
                data_height,
                screen.get_width(),
                screen.get_height() - data_height,
            )
        )

        play_border_width = play_surface.get_width() - (
            self.__square_width * self.__table_x_squares
        )

        play_border_height = play_surface.get_height() - (
            self.__square_height * self.__table_y_squares
        )

        table_surface = play_surface.subsurface(
            pg.Rect(
                play_border_width / 2,
                play_border_height / 2,
                play_surface.get_width() - play_border_width,
                play_surface.get_height() - play_border_height,
            )
        )

        self.draw_table(table_surface, snake, fruits)
        self.draw_play_border(play_surface)

    def draw_play_border(self, play_surface: pg.surface.Surface) -> None:
        play_border_width = play_surface.get_width() - (
            self.__square_width * self.__table_x_squares
        )

        play_border_height = play_surface.get_height() - (
            self.__square_height * self.__table_y_squares
        )
        pg.draw.rect(
            play_surface,
            RED_PALE,
            pg.Rect(
                0,
                0,
                play_border_width / 2,
                play_surface.get_height(),
            ),
        )

        pg.draw.rect(
            play_surface,
            RED_PALE,
            pg.Rect(
                play_surface.get_width() - (play_border_width / 2),
                0,
                play_border_width / 2,
                play_surface.get_height(),
            ),
        )

        pg.draw.rect(
            play_surface,
            RED_PALE,
            pg.Rect(
                0,
                0,
                play_surface.get_width(),
                play_border_height / 2,
            ),
        )

        pg.draw.rect(
            play_surface,
            RED_PALE,
            pg.Rect(
                0,
                play_surface.get_height() - play_border_height / 2,
                play_surface.get_width(),
                ceil(play_border_height / 2),
            ),
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
        x_pos_table_surface = x_pos_table * self.__square_width
        y_pos_table_surface = y_pos_table * self.__square_height
        pg.draw.rect(
            table_surface,
            DARK_GREEN,
            pg.Rect(
                x_pos_table_surface,
                y_pos_table_surface,
                self.__square_width,
                self.__square_height,
            ),
        )

    def draw_body(
        self, table_surface: pg.surface.Surface, x_pos_table: int, y_pos_table: int
    ) -> None:
        x_pos_table_surface = x_pos_table * self.__square_width
        y_pos_table_surface = y_pos_table * self.__square_height
        pg.draw.rect(
            table_surface,
            GREEN,
            pg.Rect(
                x_pos_table_surface,
                y_pos_table_surface,
                self.__square_width,
                self.__square_height,
            ),
        )

    def draw_fruit(
        self, table_surface: pg.surface.Surface, x_pos_table: int, y_pos_table: int
    ) -> None:
        x_pos_table_surface = x_pos_table * self.__square_width
        y_pos_table_surface = y_pos_table * self.__square_height
        pg.draw.rect(
            table_surface,
            ORANGE,
            pg.Rect(
                x_pos_table_surface,
                y_pos_table_surface,
                self.__square_width,
                self.__square_height,
            ),
        )
