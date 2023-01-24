import os
import pickle
import neat

from NeatAI.GameAI import GameAI


class AI_Controller:

    __config: neat.Config
    __game_x: int
    __game_y: int
    __draw: bool

    def __init__(self, x: int, y: int, draw: bool = False) -> None:
        self.__draw = draw
        self.__config = self.load_conf()
        self.__game_x = x
        self.__game_y = y

    def play(self, genome_name: str):
        genome = self.get_genome(genome_name)
        genome.fitness = 0  # type: ignore
        game = GameAI(self.__game_x, self.__game_y, 2, genome, self.__config)
        game.play(True)

    def get_genome(self, genome_name) -> neat.DefaultGenome:

        dirr = "NeatAI/Best_Genomes/" + str(genome_name)

        try:
            with open(dirr, "rb") as f:
                genome = pickle.load(f)
        except FileNotFoundError as e:
            print(e)
            raise SystemExit

        return genome

    def load_conf(self) -> neat.Config:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "./config.txt")

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )
        return config

    def train(self, genome_name: str, checkpoint: bool = False, max_iter: int = 200):
        if checkpoint:
            p = neat.Checkpointer.restore_checkpoint(
                f"NeatAI/Checkpoints/{genome_name}"
            )
        else:
            p = neat.Population(self.__config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(
            neat.Checkpointer(50, filename_prefix=f"NeatAI/CheckPoints/{genome_name}_")
        )

        winner = p.run(self.eval_genomes, max_iter)

        with open("NeatAI/Best_Genomes/" + genome_name, "wb") as f:
            pickle.dump(winner, f)

    def eval_genomes(self, genomes, config):

        for _genome_id, genome in genomes:
            genome.fitness = 0
            game = GameAI(self.__game_x, self.__game_y, 2, genome, config)
            self.__draw = game.play(self.__draw)
            del game
