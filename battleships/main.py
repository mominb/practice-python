from .battleships import DuplicateError, Game, OutOfRangeError


def main():
    game = Game()

    def get_attack_from_user():
        print("\033[34mEnter target position\033[0m ")
        print("_" * 30)
        x = int(input("\033[34mX-coordinates? (1-5)\033[0m  "))
        print("_" * 30)
        y = int(input("\033[34mY-coordinates? (1-5)\033[0m  "))

        return x, y

    def print_grid_and_intro(game: Game):
        print("=" * 30)
        print("\033[35mWELCOME TO BATTLESHIPS\033[0m")
        print("\033[35mDestroy all three ships to win\033[0m")
        print("=" * 30)
        for X in range(game.GRID_SIZE + 1):
            print(X, end="   ")
        print()
        for Y in range(1, Game.GRID_SIZE + 1):
            print(f"{Y}", end="   ")
            for cell in range(1, Game.GRID_SIZE + 1):
                if game.grid.get_cell(cell, Y) == "∅":
                    print(".", end="   ")
                else:
                    print(game.grid.get_cell(cell, Y), end="   ")

            print()
        print("=" * 30)

    while not game.is_over():
        print_grid_and_intro(game)
        try:
            game.attack(get_attack_from_user())
        except OutOfRangeError:
            print("\033[31mYou have entered out of range\033[0m")
        except DuplicateError:
            print("\033[31mYou have already attacked here\033[0m")
        except ValueError:
            print("\033[31mEnter numbers from 1-5 ONLY\033[0m")
    if game.is_over():
        if game._tries == 0:
            print("Game Over!!! You lost")

        else:
            print("Congrats!!! You Won.")


if __name__ == "__main__":
    main()
