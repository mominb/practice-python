import random

from grids import Grid


def main():
    ships = make_ships()
    grid = make_grid()
    run_game(grid, ships)


def make_ships():
    ships = set()
    while len(ships) != 3:
        ships.add(hide_ship())
    return tuple(ships)


def make_grid():
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


def get_attack():
    print("Enter target position")
    x = 1 + int(input("X-coordinates?  "))
    y = 6 - int(input("Y-coordinates?  "))

    return x, y


def hide_ship():
    x = random.randint(2, 6)
    y = random.randint(1, 5)

    return (x, y)


def confirm_damage(grid: Grid, attack_pos, ships):
    success = False
    print(ships)

    for ship in ships:
        if attack_pos == ship:
            (x, y) = ship
            grid.update_cell(x, y, "X")
            success = True
            break
        else:
            (x, y) = attack_pos
            grid.update_cell(x, y, "O")

    return grid, success


def run_game(grid, ships):
    remaining = 3
    tries = 10
    while remaining != 0 and tries != 0:
        print(grid)
        attack_pos = get_attack()
        grid, success = confirm_damage(grid, attack_pos, ships)
        if success:
            remaining -= 1

        tries -= 1
    if remaining == 0:
        print("ALL SHIPS DESTROYED!!! WELL DONE")
    elif tries == 0:
        print(f"{remaining} ships remain. Better luck next time :(")


if __name__ == "__main__":
    main()
