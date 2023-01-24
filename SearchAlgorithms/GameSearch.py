import numpy as np
import pygame as pg

from SnakeGame import Movements
from SnakeGame.Game import Game
from SnakeGame.Visualization import GameScreen
from .AStar import A_star_Search


class GameSearch(Game):

    def play(self):
        pg.init()
        pg.mouse.set_visible(False)
        game_screen = GameScreen(self.x_squares, self.y_squares)
        clock = pg.time.Clock()
        end = False
        why = 0
        while not end:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            snake_list = (self.table.get_snake().get_head(
            ).get_pos(), tuple([b.get_pos() for b in self.table.get_snake().get_bodies()]), self.table.get_snake().get_direction())

            movs = A_star_Search(snake_list, [f.get_pos() for f in self.table.get_fruits()], [
                                 self.x_squares, self.y_squares], )

            print(movs)
            if not movs is None:
                for mov in movs:
                    end, why = self.update_loop(mov)
                    game_screen.draw(self.table.get_snake(),
                                     self.table.get_fruits(), self.data)
                    pg.display.update()
                    clock.tick(self.frame_rate)
            else:
                end = True

            if end:
                self.end_game(why)
                break
