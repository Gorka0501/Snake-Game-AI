from dataclasses import dataclass

# (100*eaten_fruit - turns_without_eat + turns) * sqr(vel)


@dataclass
class GameData:
    score: int = 0
    turns: int = 0
    eaten_fruits: int = 0
    turns_without_eat: int = 0
    vel: int = 0
