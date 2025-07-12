import random
from enum import Enum
from typing import List, Set, Tuple


class Game:
    GRID_SIZE = 5

    def __init__(self) -> None:
        self._ships: Set[Tuple[int, int]] = Game._create_hidden_ships()
        self._attacked_positions: List[Tuple[int, int]] = []
        self.hit_count: int = 0

    @staticmethod
    def _create_hidden_ships() -> Set[Tuple[int, int]]:
        ships: Set[Tuple[int, int]] = set()

        while len(ships) != 3:
            ships.add(Game._create_a_hidden_ship())

        return ships

    def get_cell(self, x: int, y: int) -> "Game.State":
        if (x, y) in self._attacked_positions and (x, y) in self._ships:
            return Game.State.HIT
        elif (x, y) in self._attacked_positions:
            return Game.State.MISS
        else:
            return Game.State.EMPTY

    @staticmethod
    def _create_a_hidden_ship() -> Tuple[int, int]:
        x = random.randint(1, Game.GRID_SIZE)
        y = random.randint(1, Game.GRID_SIZE)

        return (x, y)

    def is_attack_repeated(self, attack_pos: Tuple[int, int]) -> bool:
        if attack_pos in self._attacked_positions:
            return True
        else:
            self._attacked_positions.append(attack_pos)
            return False

    @staticmethod
    def is_attack_in_range(attack_pos: Tuple[int, int]) -> bool:
        (x, y) = attack_pos
        if x < 1 or x > Game.GRID_SIZE or y < 1 or y > Game.GRID_SIZE:
            return False
        else:
            return True

    def is_attack_valid(self, attack_pos: Tuple[int, int]) -> None:
        if not Game.is_attack_in_range(attack_pos):
            raise OutOfRangeError()
        if self.is_attack_repeated(attack_pos):
            raise DuplicateError()
        if attack_pos in self._ships:
            self.hit_count += 1

    def is_over(self) -> bool:
        return len(self._attacked_positions) > 10 or self.hit_count == 3

    @property
    def attacked_positions(self) -> List[Tuple[int, int]]:
        return self._attacked_positions

    class State(Enum):
        HIT = 1
        MISS = 2
        EMPTY = 3


class OutOfRangeError(Exception):
    pass


class DuplicateError(Exception):
    pass
