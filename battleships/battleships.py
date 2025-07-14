import random
from enum import Enum
from typing import Set


class CellState(Enum):
    HIT = 1
    MISS = 2
    EMPTY = 3


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"


class Game:
    GRID_SIZE = 5
    NUM_SHIPS = 3
    MAX_TURNS = 10

    def __init__(self) -> None:
        self._ships: Set[Position] = self._generate_hidden_ships()
        self._attacked_positions: Set[Position] = set()

    @staticmethod
    def _is_attack_in_range(attack_pos: Position) -> bool:
        return (
            1 <= attack_pos.x <= Game.GRID_SIZE and 1 <= attack_pos.y <= Game.GRID_SIZE
        )

    @staticmethod
    def _generate_random_ship_position() -> Position:
        x = random.randint(1, Game.GRID_SIZE)
        y = random.randint(1, Game.GRID_SIZE)
        return Position(x, y)

    @staticmethod
    def _generate_hidden_ships() -> Set[Position]:
        ships: Set[Position] = set()

        while len(ships) < Game.NUM_SHIPS:
            ships.add(Game._generate_random_ship_position())

        return ships

    def _is_position_already_attacked(self, attack_pos: Position) -> bool:
        return attack_pos in self._attacked_positions

    def _count_hits(self) -> int:
        return len(self._attacked_positions & self._ships)

    def get_cell_state(self, position: Position) -> CellState:
        if position in self._attacked_positions and position in self._ships:
            return CellState.HIT
        elif position in self._attacked_positions:
            return CellState.MISS
        else:
            return CellState.EMPTY

    def attack(self, attack_pos: Position) -> CellState:
        if self.is_over:
            raise Exception("Game is over, no more attacks allowed")

        if not self._is_attack_in_range(attack_pos):
            raise OutOfRangeError(f"Attack position {attack_pos} is out of range")

        if self._is_position_already_attacked(attack_pos):
            raise DuplicateError(f"Position {attack_pos} has already been attacked")

        self._attacked_positions.add(attack_pos)

        if attack_pos in self._ships:
            return CellState.HIT
        else:
            return CellState.MISS

    @property
    def attacked_positions(self) -> Set[Position]:
        return self._attacked_positions.copy()

    @property
    def won(self) -> bool:
        return self._count_hits() >= self.NUM_SHIPS

    @property
    def lost(self) -> bool:
        return len(self._attacked_positions) >= self.MAX_TURNS

    @property
    def remaining_turns(self) -> int:
        return max(0, self.MAX_TURNS - len(self._attacked_positions))

    @property
    def is_over(self) -> bool:
        return self.won or self.lost


class OutOfRangeError(Exception):
    pass


class DuplicateError(Exception):
    pass
