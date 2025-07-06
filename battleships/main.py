from .battleships import Game


def main():
    game = Game()

    def get_attack_from_user():
        print("Enter target position")
        x = 1 + int(input("X-coordinates?  "))
        y = 6 - int(input("Y-coordinates?  "))
        return x, y

    while not game.is_over():
        print(game.grid)
        game.attack(get_attack_from_user())


if __name__ == "__main__":
    main()
