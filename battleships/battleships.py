import random

from grids import Grid


class Game:
    def __init__(self) -> None:
        self.grid = Game._make_grid()
        self._ships = Game._create_hidden_ships()
        self._ships_remaining = 3
        self._tries = 10

    @staticmethod
    def _create_hidden_ships():
        ships = set()

        while len(ships) != 3:
            ships.add(Game._create_a_hidden_ship())

        return ships

    @staticmethod
    def _create_a_hidden_ship():
        x = random.randint(2, 6)
        y = random.randint(1, 5)

        return (x, y)

    @staticmethod
    def _make_grid():
        grid = Grid(6, 6)

        for x in range(1, grid.width + 1):
            for y in range(1, grid.height + 1):
                if x == 1:
                    grid.update_cell(x, y, 6 - y)
                elif y == 6:
                    grid.update_cell(x, y, x - 1)
                else:
                    grid.update_cell(x, y, ".")
        return grid

    def attack(self, attack_pos):
        for ship in self._ships:
            if attack_pos == ship:
                (x, y) = ship
                self.grid.update_cell(x, y, "X")
                self._ships_remaining -= 1
                break
            else:
                (x, y) = attack_pos
                self.grid.update_cell(x, y, "O")

        self._tries -= 1

    def is_over(self):
        return self._tries == 0 or self._ships_remaining == 0
