from lib2to3 import pygram
import pygame as pg

from SnakeGame.Movements import Movements
from SnakeGame.SnakeTable import SnakeTable
from SnakeGame.Visualization import draw


class Game:
    __x_width: int
    __y_height: int
    __vel: int
    __table: SnakeTable

    def __init__(self, x: int, y: int, vel: int) -> None:
        self.__x_width = x
        self.__y_height = y
        self.__vel = vel
        self.__table = SnakeTable(self.__x_width, self.__y_height)

    def loop(self):
        pg.init()

        pg.mouse.set_visible(False)

        display_width = self.__y_height * 100
        display_height = self.__y_height * 100
        screen = pg.display.set_mode((display_width, display_height))

        clock = pg.time.Clock()

        end = False
        while not end:
            clock.tick(1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.__table.snake.change_direction(Movements.NORTH)
            if keys[pg.K_s]:
                self.__table.snake.change_direction(Movements.SOUTH)
            if keys[pg.K_d]:
                self.__table.snake.change_direction(Movements.WEST)
            if keys[pg.K_a]:
                self.__table.snake.change_direction(Movements.EAST)

            end, why = self.__table.update()
            matrix = self.__table.get_matrix()
            print(matrix)
            draw(
                screen,
                self.__table.snake,
                self.__table.fruits,
                (self.__table.x_width, self.__table.y_height),
            )
            pg.display.update()
            if end:
                match why:
                    case 0:
                        print(f"YOU WIN")
                    case 1:
                        print(f"YOU LOSE. \n You crashed against a wall")
                    case 2:
                        print(f"YOU LOSE. \n You ate your own tail")
                pg.quit()
