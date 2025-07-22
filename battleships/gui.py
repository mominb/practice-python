import flet as ft  # type: ignore

from .battleships import CellState, DuplicateError, Game, OutOfRangeError, Position


def main(page: ft.Page):
    page.title = "Battleships Game"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 700
    page.window.height = 800
    page.window.resizable = True
    page.bgcolor = "#1a1a1a"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Game state
    game = Game()

    # UI Controls
    game_status = ft.Text(
        "🎯 Click on grid cells to attack!",
        size=18,
        color="#74b9ff",
        weight=ft.FontWeight.W_600,
        text_align=ft.TextAlign.CENTER,
    )

    ships_counter = ft.Text(
        f"Ships Hit: {game.hits_count}/3",
        size=16,
        color="#f5f5f5",
        weight=ft.FontWeight.W_500,
    )

    attempts_counter = ft.Text(
        f"Attempts: {len(game.attacked_positions)}",
        size=16,
        color="#f5f5f5",
        weight=ft.FontWeight.W_500,
    )

    # Game Instructions
    instructions = ft.Text(
        "🎮 How to Play:\n• Click on grid cells to attack and find hidden ships\n• Find all 3 ships to win\n• You have 10 attempts maximum\n• 💥 = Hit, 💧 = Miss, 🌊 = Unexplored",
        size=14,
        color="#b0b0b0",
        weight=ft.FontWeight.W_400,
        text_align=ft.TextAlign.CENTER,
    )

    # Initialize grid container (will be set properly later)
    grid_container = ft.Container()

    def update_ui():
        """Update all UI elements with current game state"""
        ships_counter.value = f"Ships Hit: {game.hits_count}/3"
        attempts_counter.value = f"Attempts: {len(game.attacked_positions)}"
        grid_container.content = create_grid()
        page.update()  # type: ignore

    def new_game():
        """Start a new game"""
        nonlocal game
        game = Game()
        game_status.value = "🎯 Click on grid cells to attack!"
        game_status.color = "#74b9ff"
        new_game_btn.visible = False

        update_ui()

    def get_cell_size():
        """Calculate responsive cell size based on window size"""
        try:
            width = page.window.width or 700
            height = page.window.height or 800
            base_size = min(width - 100, height - 300) // (game.GRID_SIZE + 1)
            return max(40, min(80, base_size))
        except Exception:
            return 50

    def handle_cell_click(x: int, y: int):
        """Handle cell click for attacking"""
        if game.is_over:
            return

        try:
            attack_position = Position(x, y)
            cell_state = game.attack(attack_position)
            update_ui()

            if game.is_over:
                if game.won:
                    game_status.value = "🎉 Victory! All ships destroyed!"
                    game_status.color = "#00b894"
                else:
                    game_status.value = "💥 Game Over! Too many attempts!"
                    game_status.color = "#ff6b6b"
                new_game_btn.visible = True
            else:
                if cell_state == CellState.HIT:
                    game_status.value = "🎯 Direct Hit! Keep going!"
                    game_status.color = "#00b894"
                else:
                    game_status.value = "💧 Miss! Try another position."
                    game_status.color = "#74b9ff"

        except OutOfRangeError:
            game_status.value = "⚠️ Position out of range!"
            game_status.color = "#ff6b6b"
        except DuplicateError:
            game_status.value = "⚠️ Position already attacked!"
            game_status.color = "#ff6b6b"

        page.update()  # type: ignore

    def create_grid():
        """Create responsive interactive grid"""
        cell_size = get_cell_size()
        grid_rows = []

        for y in range(1, game.GRID_SIZE + 1):
            row = []
            for x in range(1, game.GRID_SIZE + 1):
                position = Position(x, y)
                cell_state = game.get_cell_state(position)

                # Dynamic cell appearance
                if cell_state == CellState.HIT:
                    cell_color = "#ff6b6b"
                    cell_text = "💥"
                elif cell_state == CellState.MISS:
                    cell_color = "#5a67d8"
                    cell_text = "💧"
                else:  # EMPTY
                    cell_color = "#2d3436"
                    cell_text = "🌊"

                cell = ft.Container(
                    content=ft.Text(
                        cell_text,
                        size=max(14, cell_size // 3),
                        weight=ft.FontWeight.W_700,
                        color="white",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=cell_size,
                    height=cell_size,
                    bgcolor=cell_color,
                    border=ft.border.all(2, "#636e72"),
                    border_radius=12,
                    alignment=ft.alignment.center,
                    on_click=lambda e, x=x, y=y: handle_cell_click(x, y),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color="#00000040",
                        offset=ft.Offset(0, 2),
                    ),
                )
                row.append(cell)  # type: ignore
            grid_rows.append(  # type: ignore
                ft.Row(row, spacing=4, alignment=ft.MainAxisAlignment.CENTER)  # type: ignore
            )

        return ft.Column(
            grid_rows,  # type: ignore
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # New Game Button
    new_game_btn = ft.ElevatedButton(
        "🎮 New Game",
        on_click=lambda e: new_game(),
        bgcolor="#74b9ff",
        color="white",
        visible=False,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(weight=ft.FontWeight.W_600, size=16),
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=4,
        ),
    )

    # Initialize grid container with actual content
    grid_container.content = create_grid()
    grid_container.alignment = ft.alignment.center

    # Main layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "🚢 BATTLESHIPS",
                            size=36,
                            weight=ft.FontWeight.W_800,
                            color="#74b9ff",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.only(bottom=10),
                    ),
                    ft.Container(
                        content=ft.Divider(color="#636e72", thickness=2),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    ft.Container(
                        content=ft.ResponsiveRow(
                            [
                                ft.Container(
                                    content=ft.Card(
                                        content=ft.Container(
                                            content=ships_counter,
                                            padding=ft.padding.all(15),
                                            alignment=ft.alignment.center,
                                        ),
                                        elevation=2,
                                        color="#a20000",
                                    ),
                                    col={"sm": 10, "md": 15},
                                ),
                                ft.Container(
                                    content=ft.Card(
                                        content=ft.Container(
                                            content=attempts_counter,
                                            padding=ft.padding.all(15),
                                            alignment=ft.alignment.center,
                                        ),
                                        elevation=2,
                                        color="#b321b6",
                                    ),
                                    col={"sm": 10, "md": 15},
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        padding=ft.padding.symmetric(vertical=15),
                    ),
                    ft.Container(
                        content=ft.Divider(color="#636e72", thickness=2),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    ft.Container(
                        content=ft.Card(
                            content=ft.Container(
                                content=instructions,
                                padding=ft.padding.all(15),
                                alignment=ft.alignment.center,
                            ),
                            elevation=2,
                        ),
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content=ft.Card(
                            content=ft.Container(
                                content=game_status,
                                padding=ft.padding.all(15),
                                alignment=ft.alignment.center,
                            ),
                            elevation=3,
                        ),
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content=new_game_btn,
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(10),
                    ),
                    ft.Container(
                        content=grid_container,
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.all(10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8081, host="0.0.0.0")  # type: ignore
