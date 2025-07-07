import random

from grids import Grid


class Game:
    GRID_SIZE = 5

    def __init__(self) -> None:
        self.grid = Grid(Game.GRID_SIZE, Game.GRID_SIZE)
        self._ships = Game._create_hidden_ships()
        self._ships_remaining = 3
        self._tries = 11
        self._attacked_positions = []

    @staticmethod
    def _create_hidden_ships():
        ships = set()

        while len(ships) != 3:
            ships.add(Game._create_a_hidden_ship())

        return ships

    @staticmethod
    def _create_a_hidden_ship():
        x = random.randint(2, Game.GRID_SIZE)
        y = random.randint(1, Game.GRID_SIZE - 1)

        return (x, y)

    def attack_repeated(self, attack_pos):
        if attack_pos in self._attacked_positions:
            return True
        else:
            self._attacked_positions.append(attack_pos)
            return False

    @staticmethod
    def is_attack_in_range(attack_pos):
        (x, y) = attack_pos
        if x <= 0 or y <= 0 or x > 5 or y > 5:
            return False
        else:
            return True

    def attack(self, attack_pos):
        if not Game.is_attack_in_range(attack_pos):
            raise OutOfRangeError()
        if self.attack_repeated(attack_pos):
            raise DuplicateError()

        if attack_pos in self._ships:
            (x, y) = attack_pos
            self.grid.update_cell(x, y, "X")
            self._ships_remaining -= 1

        else:
            (x, y) = attack_pos
            self.grid.update_cell(x, y, "O")

        self._tries -= 1

    def is_over(self):
        return self._tries == 0 or self._ships_remaining == 0


class OutOfRangeError(Exception):
    pass


class DuplicateError(Exception):
    pass
