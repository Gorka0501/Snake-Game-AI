from math import sqrt
import pygame as pg

from SnakeGame.Movements import Movements
from SnakeGame.SnakeTable import SnakeTable
from SnakeGame.Visualization import GameScreen
from SnakeGame.GameData import GameData


class Game:
    __x_squares: int
    __y_squares: int
    __vel: int
    __table: SnakeTable
    __frame_rate: int = 60
    __data: GameData = GameData()

    def __init__(self, x: int, y: int, inic_vel: int) -> None:
        self.__x_squares = x
        self.__y_squares = y
        self.__vel = inic_vel
        self.__data.vel = inic_vel
        self.__table = SnakeTable(self.__x_squares, self.__y_squares)

    def update_info(self, end: bool, eat: int) -> GameData:
        if eat == 1:
            self.__data.score += round(
                max(50 - self.__data.turns_without_eat / 2, 25) * sqrt(self.__data.vel)
            )
            self.__data.eaten_fruits += 1
            self.__data.turns_without_eat = 0
            if end:
                self.__data.score += 1000
        else:
            self.__data.turns_without_eat += 1

        self.__data.turns += 1
        return self.__data

    def loop(self):
        pg.init()

        pg.mouse.set_visible(False)
        game_screen = GameScreen(self.__x_squares, self.__y_squares)
        clock = pg.time.Clock()

        new_direction = Movements.STOP
        end = False
        why = 0
        velocity = self.__frame_rate / self.__vel
        while not end:
            clock.tick(self.__frame_rate)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                new_direction = Movements.NORTH
            if keys[pg.K_s]:
                new_direction = Movements.SOUTH
            if keys[pg.K_d]:
                new_direction = Movements.WEST
            if keys[pg.K_a]:
                new_direction = Movements.EAST
            if velocity <= 0:
                self.__table.get_snake().change_direction(new_direction)
                end, why = self.__table.update()
                self.update_info(end, why)
                velocity = self.__frame_rate / self.__vel
            velocity -= 1
            game_screen.draw(
                self.__table.get_snake(), self.__table.get_fruits(), self.__data
            )
            pg.display.update()
            if end:
                match why:
                    case 1:
                        print(f"YOU WIN")
                        print(self.__data)
                    case 0:
                        print(f"YOU LOSE. \n You crashed against a wall")
                        print(self.__data)
                    case 2:
                        print(f"YOU LOSE. \n You ate your own tail")
                        print(self.__data)
                pg.quit()
