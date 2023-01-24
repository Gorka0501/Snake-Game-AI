import tensorflow as tf
import pickle

from NeatAI.GameAI import GameAI


class AI_Controller:
    __lr: float = 1e-3
    iters: int
    __game_x: int
    __game_y: int
    __draw: bool

    def __init__(self, x: int, y: int, draw: bool = False) -> None:
        self.__draw = draw
        self.__game_x = x
        self.__game_y = y

    def create_neural_network(self, input, output):
        
