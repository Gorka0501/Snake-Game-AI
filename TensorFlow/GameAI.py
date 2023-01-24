import neat
import numpy as np
import pygame as pg

from SnakeGame import Movements
from SnakeGame.Game import Game
from SnakeGame.Visualization import GameScreen


class GameAI(Game):


    def __init__(
        self,
        x: int,
        y: int,
        inic_vel: int,
        genome: neat.DefaultGenome,
        config: neat.Config,
        frame_rate: int = 60,
    ) -> None:
        super().__init__(x, y, inic_vel, frame_rate)
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitness_function = self.update_fitness3
        self.inputs_function = self.get_inputs5
        self.movements_function = self.movements_loop2

    def get_matrix(self) -> np.ndarray:
        matrix = np.zeros(shape=(self.y_squares, self.x_squares), dtype=np.int8)

        snake_head_x_pos, snake_head_y_pos = self.table.get_snake().get_head().get_pos()
        if not matrix[snake_head_y_pos][snake_head_x_pos] == 2:
            matrix[snake_head_y_pos][snake_head_x_pos] = 1

        for body_number, body in enumerate(self.table.get_snake().get_bodies()):
            body_x_pos, body_y_pos = body.get_pos()
            if not (
                body_number == len(self.table.get_snake().get_bodies()) - 1
                and matrix[body_y_pos][body_x_pos] == 1
            ):
                matrix[body_y_pos][body_x_pos] = 2

        for fruit in self.table.get_fruits():
            fruit_x_pos, fruit_y_pos = fruit.get_pos()
            matrix[fruit_y_pos][fruit_x_pos] = 1000
        return matrix

    def update_fitness1(self) -> None:
        self.genome.fitness = self.data.score

    def update_fitness2(self, end: bool, why: int, last_direction: Movements) -> None:
        self.genome.fitness = ((self.data.eaten_fruits * 2) ** 2) + (self.data.turns**2) / 100  # type: ignore

    def update_fitness3(self, end: bool, why: int, last_direction: Movements) -> None:

        self.genome.fitness = ((self.data.eaten_fruits * 2) ** 2) * (self.data.turns**1.5) / 100  # type: ignore

    def get_inputs1(self) -> list[int]:
        return self.get_matrix().flatten()

    def get_inputs2(self) -> list[int]:

        direction = self.table.get_snake().get_direction()
        snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
        fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
        snake_body_pos = [pos.get_pos() for pos in self.table.get_snake().get_bodies()]
        return (
            1 if snake_x_pos < fruit_x_pos else 0,
            1 if snake_x_pos >= fruit_x_pos else 0,
            1
            if len(
                [
                    pos
                    for pos in snake_body_pos
                    if snake_x_pos < pos[0] and snake_y_pos == pos[1]
                ]
            )
            > 0
            else 0,
            1 if snake_x_pos > fruit_x_pos else 0,
            1 if snake_x_pos <= fruit_x_pos else 0,
            1
            if len(
                [
                    pos
                    for pos in snake_body_pos
                    if snake_x_pos > pos[0] and snake_y_pos == pos[1]
                ]
            )
            > 0
            else 0,
            1 if snake_y_pos > fruit_y_pos else 0,
            1 if snake_y_pos <= fruit_y_pos else 0,
            1
            if len(
                [
                    pos
                    for pos in snake_body_pos
                    if snake_x_pos == pos[0] and snake_y_pos > pos[1]
                ]
            )
            > 0
            else 0,
            1 if snake_y_pos < fruit_y_pos else 0,
            1 if snake_y_pos >= fruit_y_pos else 0,
            1
            if len(
                [
                    pos
                    for pos in snake_body_pos
                    if snake_x_pos == pos[0] and snake_y_pos < pos[1]
                ]
            )
            > 0
            else 0,
            1 if direction == Movements.NORTH else 0,
            1 if direction == Movements.SOUTH else 0,
            1 if direction == Movements.WEST else 0,
            1 if direction == Movements.EAST else 0,
        )

    def get_inputs3(self) -> list[int]:
        def closer_N_S_E_W() -> list[int]:
            def closer_West() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + 1, 0)
                if snake_x_pos < fruit_x_pos and snake_y_pos == fruit_y_pos:
                    closer = (fruit_x_pos, 1)

                min_dist_body = min(
                    [
                        pos[0]
                        for pos in snake_body_pos
                        if snake_x_pos < pos[0] and snake_y_pos == pos[1]
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = self.x_squares - snake_x_pos
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_East() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + 1, 0)

                if snake_x_pos > fruit_x_pos and snake_y_pos == fruit_y_pos:
                    closer = (fruit_x_pos, 1)

                min_dist_body = min(
                    [
                        pos[0]
                        for pos in snake_body_pos
                        if snake_x_pos > pos[0] and snake_y_pos == pos[1]
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = snake_x_pos
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_South() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.y_squares + 1, 0)
                if snake_y_pos < fruit_y_pos and snake_x_pos == fruit_x_pos:
                    closer = (fruit_y_pos, 1)

                min_dist_body = min(
                    [
                        pos[0]
                        for pos in snake_body_pos
                        if snake_y_pos < pos[0] and snake_x_pos == pos[1]
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = self.y_squares - snake_y_pos
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_North() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.y_squares + 1, 0)
                if snake_y_pos > fruit_y_pos and snake_x_pos == fruit_x_pos:
                    closer = (fruit_y_pos, 1)
                min_dist_body = min(
                    [
                        pos[0]
                        for pos in snake_body_pos
                        if snake_y_pos > pos[0] and snake_x_pos == pos[1]
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = snake_y_pos

                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            return_array = (
                closer_North() + closer_East() + closer_South() + closer_West()
            )
            return return_array

        def closer_NE_SE_SW_SW() -> list[int]:
            def closer_NorthEast() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + self.y_squares + 1, 0)

                if (
                    snake_x_pos > fruit_x_pos
                    and snake_y_pos > fruit_y_pos
                    and abs(snake_x_pos - fruit_x_pos) == abs(snake_y_pos - fruit_y_pos)
                ):
                    closer = (
                        abs(snake_x_pos - fruit_x_pos) + abs(snake_y_pos - fruit_y_pos),
                        1,
                    )

                min_dist_body = min(
                    [
                        abs(snake_x_pos - body_x_pos) + abs(snake_y_pos - body_y_pos)
                        for body_x_pos, body_y_pos in snake_body_pos
                        if snake_x_pos > body_x_pos
                        and snake_y_pos > body_y_pos
                        and abs(snake_x_pos - body_x_pos)
                        == abs(snake_y_pos - body_y_pos)
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = snake_x_pos + snake_y_pos
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_SouthEast() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + self.y_squares + 1, 0)

                if (
                    snake_x_pos > fruit_x_pos
                    and snake_y_pos < fruit_y_pos
                    and abs(snake_x_pos - fruit_x_pos) == abs(snake_y_pos - fruit_y_pos)
                ):
                    closer = (
                        abs(snake_x_pos - fruit_x_pos) + abs(snake_y_pos - fruit_y_pos),
                        1,
                    )

                min_dist_body = min(
                    [
                        abs(snake_x_pos - body_x_pos) + abs(snake_y_pos - body_y_pos)
                        for body_x_pos, body_y_pos in snake_body_pos
                        if snake_x_pos > body_x_pos
                        and snake_y_pos < body_y_pos
                        and abs(snake_x_pos - body_x_pos)
                        == abs(snake_y_pos - body_y_pos)
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = snake_x_pos + abs(snake_y_pos - self.y_squares)
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_SouthWest() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + self.y_squares + 1, 0)

                if (
                    snake_x_pos < fruit_x_pos
                    and snake_y_pos < fruit_y_pos
                    and abs(snake_x_pos - fruit_x_pos) == abs(snake_y_pos - fruit_y_pos)
                ):
                    closer = (
                        abs(snake_x_pos - fruit_x_pos) + abs(snake_y_pos - fruit_y_pos),
                        1,
                    )

                min_dist_body = min(
                    [
                        abs(snake_x_pos - body_x_pos) + abs(snake_y_pos - body_y_pos)
                        for body_x_pos, body_y_pos in snake_body_pos
                        if snake_x_pos < body_x_pos
                        and snake_y_pos < body_y_pos
                        and abs(snake_x_pos - body_x_pos)
                        == abs(snake_y_pos - body_y_pos)
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = abs(snake_x_pos - self.x_squares) + abs(
                    snake_y_pos - self.y_squares
                )
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            def closer_NorthWest() -> list[int]:
                snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
                fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
                snake_body_pos = [
                    pos.get_pos() for pos in self.table.get_snake().get_bodies()
                ]
                closer = (self.x_squares + self.y_squares + 1, 0)

                if (
                    snake_x_pos < fruit_x_pos
                    and snake_y_pos > fruit_y_pos
                    and abs(snake_x_pos - fruit_x_pos) == abs(snake_y_pos - fruit_y_pos)
                ):
                    closer = (
                        abs(snake_x_pos - fruit_x_pos) + abs(snake_y_pos - fruit_y_pos),
                        1,
                    )

                min_dist_body = min(
                    [
                        abs(snake_x_pos - body_x_pos) + abs(snake_y_pos - body_y_pos)
                        for body_x_pos, body_y_pos in snake_body_pos
                        if snake_x_pos < body_x_pos
                        and snake_y_pos > body_y_pos
                        and abs(snake_x_pos - body_x_pos)
                        == abs(snake_y_pos - body_y_pos)
                    ]
                    + [self.x_squares * self.y_squares]
                )
                if min_dist_body < closer[0]:
                    closer = (min_dist_body, 2)

                border_dist = abs(snake_x_pos - self.x_squares) + snake_y_pos
                if border_dist <= 1:
                    closer = (border_dist, 3)

                return_array = [0] * 4
                return_array[closer[1]] = 1
                return return_array

            return_array = (
                closer_NorthEast()
                + closer_SouthEast()
                + closer_SouthWest()
                + closer_NorthWest()
            )
            return return_array

        direction = self.table.get_snake().get_direction()
        return_array = (
            closer_N_S_E_W()
            + closer_NE_SE_SW_SW()
            + [
                1 if direction == Movements.NORTH else 0,
                1 if direction == Movements.SOUTH else 0,
                1 if direction == Movements.WEST else 0,
                1 if direction == Movements.EAST else 0,
            ]
        )
        return return_array

    def get_inputs4(self) -> list[int]:
        def dist_N() -> int:
            space = 0
            for i in range(0, snake_y_pos)[::-1]:
                if (snake_x_pos, i) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_S() -> int:
            space = 0
            for i in range(snake_y_pos + 1, self.y_squares + 1, 1):
                if (snake_x_pos, i) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_E() -> int:
            space = 0
            for i in range(0, snake_x_pos)[::-1]:
                if (i, snake_y_pos) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_W() -> int:
            space = 0
            for i in range(snake_x_pos + 1, self.x_squares + 1, 1):
                if (i, snake_y_pos) in snake_body_pos:
                    break
                space += 1
            return space

        direction = self.table.get_snake().get_direction()
        snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
        fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
        snake_body_pos = [pos.get_pos() for pos in self.table.get_snake().get_bodies()]
        manhattan_distance_N = snake_y_pos - fruit_y_pos
        manhattan_distance_S = -snake_y_pos + fruit_y_pos
        manhattan_distance_E = snake_x_pos - fruit_x_pos
        manhattan_distance_W = -snake_x_pos + fruit_x_pos
        return_array = [
            manhattan_distance_N,
            manhattan_distance_S,
            manhattan_distance_E,
            manhattan_distance_W,
            dist_N(),
            dist_S(),
            dist_E(),
            dist_W(),
            self.table.get_snake().get_length(),
        ]
        return return_array

    def get_inputs5(self) -> list[int]:
        direction = self.table.get_snake().get_direction()
        snake_x_pos, snake_y_pos = self.table.get_snake().get_head().get_pos()
        fruit_x_pos, fruit_y_pos = self.table.get_fruits()[0].get_pos()
        snake_body_pos = [pos.get_pos() for pos in self.table.get_snake().get_bodies()]

        def dist_N() -> int:
            space = 0
            for i in range(0, snake_y_pos)[::-1]:
                if (snake_x_pos, i) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_S() -> int:
            space = 0
            for i in range(snake_y_pos + 1, self.y_squares + 1, 1):
                if (snake_x_pos, i) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_E() -> int:
            space = 0
            for i in range(0, snake_x_pos)[::-1]:
                if (i, snake_y_pos) in snake_body_pos:
                    break
                space += 1
            return space

        def dist_W() -> int:
            space = 0
            for i in range(snake_x_pos + 1, self.x_squares + 1, 1):
                if (i, snake_y_pos) in snake_body_pos:
                    break
                space += 1
            return space

        def get_North() -> list[int]:
            x = snake_x_pos - fruit_x_pos
            y = snake_y_pos - fruit_y_pos
            return x, y

        def get_South() -> list[int]:
            x = -snake_x_pos + fruit_x_pos
            y = -snake_y_pos + fruit_y_pos
            return x, y

        def get_East() -> list[int]:
            x = snake_x_pos - fruit_x_pos
            y = -snake_y_pos + fruit_y_pos
            return x, y

        def get_West() -> list[int]:
            x = -snake_x_pos + fruit_x_pos
            y = snake_y_pos - fruit_y_pos
            return x, y

        direction = self.table.get_snake().get_direction()
        return_array = []
        match direction:
            case Movements.STOP:
                return_array = [
                    *get_North(),
                    dist_N(),
                    dist_E(),
                    dist_S(),
                    dist_W(),
                    1,
                    0,
                    0,
                    0,
                ]
            case Movements.NORTH:
                return_array = [
                    *get_North(),
                    dist_N(),
                    dist_E(),
                    dist_S(),
                    dist_W(),
                    1,
                    0,
                    0,
                    0,
                ]
            case Movements.SOUTH:
                return_array = [
                    *get_South(),
                    dist_S(),
                    dist_W(),
                    dist_N(),
                    dist_E(),
                    0,
                    0,
                    1,
                    0,
                ]
            case Movements.EAST:
                return_array = [
                    *get_East(),
                    dist_E(),
                    dist_S(),
                    dist_W(),
                    dist_N(),
                    0,
                    1,
                    0,
                    0,
                ]
            case Movements.WEST:
                return_array = [
                    *get_West(),
                    dist_W(),
                    dist_N(),
                    dist_E(),
                    dist_S(),
                    0,
                    0,
                    0,
                    1,
                ]

        return return_array

    def movements_loop1(self, last_movement: Movements) -> Movements:
        output = self.net.activate(self.inputs_function())
        decision = output.index(max(output))
        new_direction = last_movement
        match decision:
            case 0:
                new_direction = Movements.NORTH
            case 1:
                new_direction = Movements.SOUTH
            case 2:
                new_direction = Movements.WEST
            case 3:
                new_direction = Movements.EAST
        return new_direction

    def movements_loop2(self, last_movement: Movements) -> Movements:
        output = self.net.activate(self.inputs_function())
        decision = output.index(max(output))
        new_direction = last_movement
        match decision:
            case 0:
                match last_movement:
                    case Movements.NORTH:
                        new_direction = Movements.WEST
                    case Movements.WEST:
                        new_direction = Movements.SOUTH
                    case Movements.SOUTH:
                        new_direction = Movements.WEST
                    case Movements.EAST:
                        new_direction = Movements.NORTH
            case 1:
                match last_movement:
                    case Movements.NORTH:
                        new_direction = Movements.EAST
                    case Movements.EAST:
                        new_direction = Movements.SOUTH
                    case Movements.SOUTH:
                        new_direction = Movements.WEST
                    case Movements.WEST:
                        new_direction = Movements.NORTH
            case 2:
                new_direction = last_movement

        return new_direction

    def draw(self, game_screen: GameScreen) -> None:
        game_screen.draw(self.table.get_snake(), self.table.get_fruits(), self.data)
        pg.display.update()

    def play(self, draw: bool = False) -> bool:
        pg.init()
        is_game_screen = False
        clock = pg.time.Clock()
        end = False
        why = 0
        new_direction = Movements.NORTH
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        draw = not draw

            last_direction = self.table.get_snake().get_direction()
            new_direction = self.movements_function(new_direction)
            end, why = self.update_loop(new_direction)

            if self.data.turns_without_eat >= self.x_squares * self.y_squares:  # type: ignore
                end = True
                why = 3

            if draw:
                if not is_game_screen:
                    game_screen = GameScreen(self.x_squares, self.y_squares)
                try:
                    self.draw(game_screen)  # type: ignore
                    clock.tick(self.vel)
                except NameError:
                    is_game_screen = False
            if end:
                self.fitness_function(end, why, last_direction)
                return draw
