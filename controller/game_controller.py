class GameController:
    def __init__(self, model, view, test_board, test_mode=False):
        """
        Initializes the controller with a game model and view.
        """
        self.model = model
        self.view = view
        self.test_mode = test_mode
        self.test_board = test_board

    def reveal_cell(self, x, y):
        """
        Handles revealing a cell.
        """
        result = self.model.reveal_cell(x, y)
        self.view.update_cell(x, y)

        # Reveal surrounding empty cells if needed
        cell = self.model.board[x][y]
        if cell.adjacent_mines == 0:
            self.model.reveal_empty_cells(x, y, self.view.update_cell)

        if result == "LOSS":
            self.view.display_game_over(False)
        elif result == "WIN" or result == "WIN_TREASURE":  # Updated to handle treasure win
            self.view.display_game_over(result)  # Pass the specific win condition

    def toggle_flag(self, x, y):
        """
        Handles toggling a flag on a cell.
        """
        self.model.toggle_flag(x, y)
        self.view.update_cell(x, y)
        self.view.update_flags_label()

    def restart_game(self):
        """Restarts the game by resetting the model and refreshing the view."""
        self.model.reset_game()
        if self.test_mode:
            print('Log: In test mode')
            self.model.initialize_test_board(self.test_board)
        else:
            print('Log: In normal mode')
            self.model.initialize_board()
        self.model.start_time = None

        # Update view based on type
        if hasattr(self.view, "setup_board"):  # GUI View
            self.view.setup_board()
            self.view.start_timer()
            # Update GUI elements only for GUI view
            self.view.labels["mines"].config(text=f"Mines: {self.model.mines_count}")
            self.view.update_flags_label()
        elif hasattr(self.view, "reset_view"):  # Text View
            self.view.reset_view()

    def run(self):
        """
        Starts the main game loop (for console-based view).
        """
        self.view.run()