from math import sqrt
import pygame as pg

from SnakeGame.Movements import Movements
from SnakeGame.SnakeTable import SnakeTable
from SnakeGame.Visualization import GameScreen
from SnakeGame.GameData import GameData


class Game:
    x_squares: int
    y_squares: int
    vel: int
    table: SnakeTable
    frame_rate: int = 60
    data: GameData = GameData()

    def __init__(self, x: int, y: int, inic_vel: int, frame_rate: int = 60) -> None:
        self.frame_rate = frame_rate
        self.x_squares = x
        self.y_squares = y
        self.vel = min(frame_rate, inic_vel)
        self.data = GameData()
        self.data.vel = inic_vel
        self.table = SnakeTable(self.x_squares, self.y_squares)

    def update_info(self, end: bool, eat: int) -> GameData:
        if eat == 1:
            self.data.score += round(max(50 - self.data.turns_without_eat / 2, 0))
            self.data.eaten_fruits += 1
            self.data.turns_without_eat = 0
            if end:
                self.data.score += 1000
        else:
            self.data.turns_without_eat += 1

        self.data.turns += 1
        return self.data

    def update_loop(self, new_direction: Movements) -> tuple[bool, int]:
        self.table.get_snake().change_direction(new_direction)
        end, why = self.table.update()
        self.update_info(end, why)
        return end, why

    def movements_loop(self, last_movement: Movements) -> Movements:

        keys = pg.key.get_pressed()
        new_direction = last_movement
        if keys[pg.K_w]:
            new_direction = Movements.NORTH
        if keys[pg.K_s]:
            new_direction = Movements.SOUTH
        if keys[pg.K_d]:
            new_direction = Movements.WEST
        if keys[pg.K_a]:
            new_direction = Movements.EAST
        return new_direction

    def end_game(self, why: int) -> None:
        match why:
            case 1:
                print(f"YOU WIN")
                print(self.data)
            case 0:
                print(f"YOU LOSE. \n You crashed against a wall")
                print(self.data)
            case 2:
                print(f"YOU LOSE. \n You ate your own tail")
                print(self.data)
        pg.quit()

    def play(self):
        pg.init()
        pg.mouse.set_visible(False)
        game_screen = GameScreen(self.x_squares, self.y_squares)

        clock = pg.time.Clock()
        end = False
        why = 0
        velocity = self.frame_rate / self.vel
        new_direction = Movements.STOP
        while not end:
            clock.tick(self.frame_rate)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            new_direction = self.movements_loop(new_direction)
            if velocity <= 0:
                end, why = self.update_loop(new_direction)
                velocity = self.frame_rate / self.vel
            velocity -= 1

            game_screen.draw(self.table.get_snake(), self.table.get_fruits(), self.data)
            pg.display.update()
            if end:
                self.end_game(why)
                break
