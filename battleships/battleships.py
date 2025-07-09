import random
from enum import Enum


class Game:
    GRID_SIZE = random.randint(4, 6)

    def __init__(self) -> None:
        self._ships = Game._create_hidden_ships()
        self._attacked_positions = []
        self._hit_count = 0

    @staticmethod
    def _create_hidden_ships():
        ships = set()

        while len(ships) != 3:
            ships.add(Game._create_a_hidden_ship())

        return ships

    def get_cell(self, x, y):
        if (x, y) in self._attacked_positions and (x, y) in self._ships:
            return Game.State.HIT
        elif (x, y) in self._attacked_positions:
            return Game.State.MISS
        else:
            return Game.State.EMPTY

    @staticmethod
    def _create_a_hidden_ship():
        x = random.randint(1, Game.GRID_SIZE)
        y = random.randint(1, Game.GRID_SIZE)

        return (x, y)

    def is_attack_repeated(self, attack_pos):
        if attack_pos in self._attacked_positions:
            return True
        else:
            self._attacked_positions.append(attack_pos)
            return False

    @staticmethod
    def is_attack_in_range(attack_pos):
        (x, y) = attack_pos
        if 1 > x > Game.GRID_SIZE or 1 > y > Game.GRID_SIZE:
            return False
        else:
            return True

    def is_attack_valid(self, attack_pos):
        if not Game.is_attack_in_range(attack_pos):
            raise OutOfRangeError()
        if self.is_attack_repeated(attack_pos):
            raise DuplicateError()
        if attack_pos in self._ships:
            self._hit_count += 1

    def is_over(self):
        return len(self._attacked_positions) > 10 or self._hit_count == 3

    class State(Enum):
        HIT = 1
        MISS = 2
        EMPTY = 3


class OutOfRangeError(Exception):
    pass


class DuplicateError(Exception):
    pass
