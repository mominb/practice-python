import unittest
from unittest.mock import MagicMock, patch

from .battleships import CellState, Game, Position


class TestPosition(unittest.TestCase):
    """Test cases for the Position class."""

    def test_position_initialization(self):
        position = Position(1, 3)
        self.assertEqual(position.x, 1)
        self.assertEqual(position.y, 3)

    def test_position_equality(self):
        position = Position(1, 3)
        position1 = Position(1, 3)
        self.assertEqual(position, position1)

    def test_position_inequality(self):
        position = Position(1, 3)
        position1 = Position(1, 2)
        self.assertNotEqual(position, position1)

    def test_position_equality_with_non_position_object(self):
        position = Position(1, 3)
        self.assertNotEqual(position, (1, 3))

    def test_position_hash(self):
        position = Position(1, 3)
        self.assertEqual(position.__hash__, position.__hash__)

    def test_position_hash_different_coordinates(self):
        position = Position(1, 3)
        position1 = Position(1, 2)
        self.assertNotEqual(position.__hash__, position1.__hash__)

    def test_position_repr(self):
        position = Position(1, 3)
        self.assertEqual(position.__repr__(), "Position(1, 3)")


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""

    def setUp(self):
        self.game = Game()

    def test_game_initialization(self):
        self.assertIsInstance(self.game, Game)

    def test_game_constants(self):
        self.assertEqual(self.game.GRID_SIZE, 5)
        self.assertEqual(self.game.NUM_SHIPS, 3)
        self.assertEqual(self.game.MAX_TURNS, 10)


class TestGameStaticMethods(unittest.TestCase):
    def test_is_attack_in_range_valid_positions(self):
        valid_positions = [
            Position(1, 1),
            Position(1, 5),
            Position(5, 1),
            Position(5, 5),
            Position(3, 3),
            Position(2, 4),
            Position(4, 2),
        ]
        for position in valid_positions:
            self.assertTrue(Game._is_attack_in_range(position))  # type: ignore

    def test_is_attack_in_range_invalid_positions_below_range(self):
        invalid_positions = [
            Position(0, 1),
            Position(1, 0),
            Position(0, 0),
            Position(-1, 1),
            Position(1, -1),
            Position(-1, -1),
        ]
        for position in invalid_positions:
            self.assertFalse(Game._is_attack_in_range(position))  # type: ignore

    def test_is_attack_in_range_invalid_positions_above_range(self):
        """Test that positions with coordinates greater than GRID_SIZE are considered out of range."""
        invalid_positions = [
            Position(6, 1),
            Position(1, 6),
            Position(6, 6),
            Position(10, 5),
            Position(5, 10),
            Position(10, 10),
        ]
        for position in invalid_positions:
            self.assertFalse(Game._is_attack_in_range(position))  # type: ignore

    def test_is_attack_in_range_boundary_positions(self):
        """Test that boundary positions (1,1), (1,5), (5,1), (5,5) are considered in range."""
        boundary_positions = [
            Position(1, 1),
            Position(1, 5),
            Position(5, 1),
            Position(5, 5),
        ]
        for position in boundary_positions:
            self.assertTrue(Game._is_attack_in_range(position))  # type: ignore

    @patch("battleships.random.randint")
    def test_generate_random_ship_position(self, mock_randint: MagicMock) -> None:
        """Test that random ship position generation returns Position within grid bounds."""
        self.fail("Test not implemented yet")

    @patch("battleships.Game._generate_random_ship_position")
    def test_generate_hidden_ships_correct_count(
        self, mock_generate_position: MagicMock
    ) -> None:
        """Test that exactly NUM_SHIPS ships are generated."""
        self.fail("Test not implemented yet")

    @patch("battleships.Game._generate_random_ship_position")
    def test_generate_hidden_ships_unique_positions(
        self, mock_generate_position: MagicMock
    ) -> None:
        """Test that all generated ship positions are unique (no duplicates)."""
        self.fail("Test not implemented yet")

    @patch("battleships.Game._generate_random_ship_position")
    def test_generate_hidden_ships_handles_duplicate_generation(
        self, mock_generate_position: MagicMock
    ) -> None:
        """Test that ship generation handles duplicate random positions correctly."""
        self.fail("Test not implemented yet")


class TestGameAttackValidation(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_is_position_already_attacked_fresh_position(self):
        position = Position(2, 3)
        self.assertFalse(self.game._is_position_already_attacked(position))  # type: ignore

    def test_is_position_already_attacked_attacked_position(self):
        position = Position(2, 3)
        self.game._attacked_positions.add(position)  # type: ignore # Use _attacked_positions instead
        self.assertTrue(self.game._is_position_already_attacked(position))  # type: ignore


class TestGameCellState(unittest.TestCase):
    """Test cases for Game cell state retrieval."""

    def setUp(self):
        self.game = Game()

    def test_get_cell_state_empty_unattacked(self):
        """Test that unattacked positions return EMPTY state."""
        position = Position(2, 3)
        self.assertEqual(self.game.get_cell_state(position), CellState.EMPTY)

    def test_get_cell_state_hit(self):
        """Test that attacked ship positions return HIT state."""
        position = Position(2, 3)
        self.game._ships.add(position)  # type: ignore
        self.game._attacked_positions.add(position)  # type: ignore
        self.assertEqual(self.game.get_cell_state(position), CellState.HIT)

    def test_get_cell_state_miss(self):
        """Test that attacked non-ship positions return MISS state."""
        position = Position(2, 3)
        self.game._attacked_positions.add(position)  # type: ignore
        self.assertEqual(self.game.get_cell_state(position), CellState.MISS)


class TestGameAttack(unittest.TestCase):
    """Test cases for Game attack functionality."""

    def setUp(self):
        self.game = Game()
        self.game._ships = {Position(1, 1), Position(2, 2), Position(3, 3)}  # type: ignore

    def test_attack_hit(self):
        """Test attacking a ship position returns HIT."""
        result = self.game.attack(Position(1, 1))
        self.assertEqual(result, CellState.HIT)

    def test_attack_miss(self):
        """Test attacking empty position returns MISS."""
        result = self.game.attack(Position(4, 4))
        self.assertEqual(result, CellState.MISS)

    def test_attack_out_of_range(self):
        """Test attacking out-of-range position raises exception."""
        with self.assertRaises(Exception):
            self.game.attack(Position(0, 0))

    def test_attack_duplicate(self):
        """Test attacking same position twice raises exception."""
        self.game.attack(Position(1, 1))
        with self.assertRaises(Exception):
            self.game.attack(Position(1, 1))

    def test_attack_when_won(self):
        """Test attacking when game is won raises exception."""
        for ship_pos in self.game._ships:  # type: ignore
            self.game.attack(ship_pos)
        with self.assertRaises(Exception):
            self.game.attack(Position(4, 4))

    def test_attack_updates_positions(self):
        """Test attack adds position to attacked_positions."""
        position = Position(1, 1)
        self.game.attack(position)
        self.assertIn(position, self.game.attacked_positions)


class TestGameProperties(unittest.TestCase):
    """Test cases for Game property methods."""

    def setUp(self):
        self.game = Game()
        self.position = Position(1, 1)
        self.game._ships = {self.position, Position(2, 2), Position(3, 3)}  # type: ignore

    def test_hits_count_no_hits(self):
        """Test that hits_count returns correct number when no ships have been hit."""
        self.assertEqual(self.game.hits_count, 0)

    def test_hits_count_some_hits(self):
        """Test that hits_count returns correct number when some ships have been hit."""
        self.game.attack(self.position)  # type: ignore
        self.assertEqual(self.game.hits_count, 1)

    def test_hits_count_all_hits(self):
        """Test that hits_count returns NUM_SHIPS when all ships have been hit."""
        for position in self.game._ships:  # type: ignore
            self.game.attack(position)

        self.assertEqual(self.game.hits_count, self.game.NUM_SHIPS)

    def test_attacked_positions_returns_copy(self):
        """Test that attacked_positions property returns a copy, not the original set."""
        self.assertFalse(self.game.attacked_positions is self.game._attacked_positions)  # type: ignore

    def test_attacked_positions_reflects_attacks(self):
        """Test that attacked_positions contains all positions that have been attacked."""
        self.game.attack(self.position)  # type: ignore
        self.assertTrue(self.position in self.game.attacked_positions)

    def test_won_property_false_when_not_all_ships_hit(self):
        """Test that won property returns False when not all ships have been hit."""
        self.game.attack(self.position)
        self.assertFalse(self.game.won)

    def test_won_property_true_when_all_ships_hit(self):
        """Test that won property returns True when all ships have been hit."""
        for position in self.game._ships:  # type: ignore
            self.game.attack(position)
        self.assertTrue(self.game.won)

    def test_lost_property_false_when_turns_remaining(self):
        """Test that lost property returns False when turns are still available."""
        self.fail("Test not implemented yet")

    def test_lost_property_true_when_max_turns_reached(self):
        """Test that lost property returns True when MAX_TURNS attacks have been made."""
        self.fail("Test not implemented yet")

    def test_remaining_turns_full_turns_available(self):
        """Test that remaining_turns returns MAX_TURNS when no attacks have been made."""
        self.fail("Test not implemented yet")

    def test_remaining_turns_some_turns_used(self):
        """Test that remaining_turns decreases correctly as attacks are made."""
        self.fail("Test not implemented yet")

    def test_remaining_turns_no_turns_remaining(self):
        """Test that remaining_turns returns 0 when MAX_TURNS attacks have been made."""
        self.fail("Test not implemented yet")

    def test_remaining_turns_never_negative(self):
        """Test that remaining_turns never returns negative values."""
        self.fail("Test not implemented yet")

    def test_is_over_false_when_game_active(self):
        """Test that is_over returns False when game is still active."""
        self.fail("Test not implemented yet")

    def test_is_over_true_when_won(self):
        """Test that is_over returns True when game is won."""
        self.fail("Test not implemented yet")

    def test_is_over_true_when_lost(self):
        """Test that is_over returns True when game is lost."""
        self.fail("Test not implemented yet")


class TestGameScenarios(unittest.TestCase):
    """Test cases for complete game scenarios."""

    def setUp(self):
        self.game = Game()
        self.game._ships = {Position(1, 1), Position(2, 2), Position(3, 3)}  # type: ignore

    def test_winning_game(self):
        """Test winning by hitting all ships."""
        for ship_pos in self.game._ships:  # type: ignore
            self.game.attack(ship_pos)

        self.assertTrue(self.game.won)
        self.assertTrue(self.game.is_over)

    def test_losing_game(self):
        """Test losing by running out of turns."""

        self.game._attacked_positions = {  # type: ignore
            Position(1, 2),
            Position(1, 3),
            Position(1, 4),
            Position(1, 5),
            Position(2, 1),
            Position(2, 3),
            Position(2, 4),
            Position(2, 5),
            Position(3, 1),
            Position(3, 2),
        }

        self.assertTrue(self.game.lost)
        self.assertTrue(self.game.is_over)


if __name__ == "__main__":
    unittest.main()
