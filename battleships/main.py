from .battleships import DuplicateError, Game, OutOfRangeError


def main():
    game = Game()

    def get_attack_from_user():
        print("\033[34mEnter target position\033[0m ")
        print("_" * 30)
        x = int(input("\033[34mX-coordinates? \033[0m  "))
        print("_" * 30)
        y = int(input("\033[34mY-coordinates? \033[0m  "))

        return x, y

    def print_intro():
        print("=" * 30)
        print("\033[35mWELCOME TO BATTLESHIPS\033[0m")
        print("\033[35mDestroy all three ships to win\033[0m")
        print(f"\033[35mDifficulty {game.GRID_SIZE - 3}\033[0m")
        print("=" * 30)

    def print_grid(game: Game):
        for X in range(game.GRID_SIZE + 1):
            print(X, end="   ")
        print()
        for Y in range(1, Game.GRID_SIZE + 1):
            print(f"{Y}", end="   ")
            for cell in range(1, Game.GRID_SIZE + 1):
                if game.get_cell(cell, Y) == Game.State.EMPTY:
                    print(".", end="   ")
                elif game.get_cell(cell, Y) == Game.State.MISS:
                    print("O", end="   ")
                elif game.get_cell(cell, Y) == Game.State.HIT:
                    print("X", end="   ")

            print()
        print("=" * 30)

    while not game.is_over():
        print_intro()
        print_grid(game)
        try:
            game.is_attack_valid(get_attack_from_user())
        except OutOfRangeError:
            print("\033[31mYou have entered out of range\033[0m")
        except DuplicateError:
            print("\033[31mYou have already attacked here\033[0m")
        except ValueError:
            print("\033[31mEnter numbers ONLY\033[0m")
    if game.is_over():
        if len(game.attacked_positions) > 10:
            print()
            print("Game Over!!! You lost")
            print()

        elif game.hit_count == 3:
            print("\033[32mCongrats!!! You Won.\033[0m")
            print()
            print("=" * 30)
            print_grid(game)


if __name__ == "__main__":
    main()
