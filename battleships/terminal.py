from colorama import Fore, Style, init

from .battleships import CellState, DuplicateError, Game, OutOfRangeError, Position

# Initialize colorama for cross-platform support
init(autoreset=True)


# UI Style Constants - Semantic naming based on purpose
class Styles:
    PROMPT = f"{Fore.BLUE}"
    TITLE = f"{Fore.MAGENTA}{Style.BRIGHT}"
    COORDINATES = f"{Fore.WHITE}{Style.BRIGHT}"
    EMPTY_CELL = f"{Fore.CYAN}"
    MISS_CELL = f"{Fore.YELLOW}"
    HIT_CELL = f"{Fore.RED}{Style.BRIGHT}"
    ERROR = f"{Fore.RED}"
    SUCCESS = f"{Fore.GREEN}{Style.BRIGHT}"


def main():
    game = Game()

    def get_attack_from_user():
        print(f"{Styles.PROMPT}Enter target position")
        print("_" * 30)
        x = int(input(f"{Styles.PROMPT}X-coordinates? "))
        print("_" * 30)
        y = int(input(f"{Styles.PROMPT}Y-coordinates? "))

        return Position(x, y)

    def print_intro():
        print("=" * 30)
        print(f"{Styles.TITLE}WELCOME TO BATTLESHIPS")
        print(f"{Styles.TITLE}Destroy all three ships to win")
        print("=" * 30)

    def cell_state_to_string(cell_state: CellState) -> str:
        match cell_state:
            case CellState.EMPTY:
                return f"{Styles.EMPTY_CELL}."
            case CellState.MISS:
                return f"{Styles.MISS_CELL}O"
            case CellState.HIT:
                return f"{Styles.HIT_CELL}X"
            case _:
                raise ValueError("Unknown cell state")

    def print_grid(game: Game):
        for x in range(game.GRID_SIZE + 1):
            if x == 0:
                print(" ", end="   ")
            else:
                print(f"{Styles.COORDINATES}{x}", end="   ")
        print()

        for y in range(1, Game.GRID_SIZE + 1):
            print(f"{Styles.COORDINATES}{y}", end="   ")
            for cell in range(1, Game.GRID_SIZE + 1):
                cell_state_string = cell_state_to_string(
                    game.get_cell_state(Position(cell, y))
                )
                print(cell_state_string, end="   ")
            print()
        print("=" * 30)

    while not game.is_over:
        print_intro()
        print_grid(game)
        try:
            game.attack(get_attack_from_user())
        except OutOfRangeError:
            print(f"{Styles.ERROR}You have entered out of range")
        except DuplicateError:
            print(f"{Styles.ERROR}You have already attacked here")
        except ValueError:
            print(f"{Styles.ERROR}Enter numbers ONLY")

    if game.is_over:
        if game.lost:
            print()
            print("Game Over!!! You lost")
            print()

        elif game.won:
            print(f"{Styles.SUCCESS}Congrats!!! You Won.")
            print()
            print("=" * 30)
            print_grid(game)


if __name__ == "__main__":
    main()
