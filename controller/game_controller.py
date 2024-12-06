class GameController:
    """
    Controls game logic and mediates between model and view components.
    
    Invariants:
        - model must be a valid GameModel instance
        - view must be a valid View instance
        - test_board must be valid when test_mode is True
    """
    def __init__(self, model, view, test_board, test_mode=False):
        """
        Initializes the controller with a game model and view.
        
        Precondition:
            - model must be a valid GameModel instance
            - view must be a valid View instance
            - test_board must be a valid 2D list when test_mode is True
        Postcondition:
            - Controller is initialized with valid model and view references
            - Test mode is properly configured if enabled
        Invariant:
            - Model and view references remain constant
        
        Maps to: __init__ in original minesweeper.py Minesweeper class
        """
        self.model = model
        self.view = view
        self.test_mode = test_mode
        self.test_board = test_board

    def reveal_cell(self, x, y):
        """
        Handles revealing a cell.
        
        Precondition:
            - x and y must be valid board coordinates
            - Cell at (x,y) must not be revealed or flagged
        Postcondition:
            - Cell is revealed and view is updated
            - Game state is updated if win/loss condition met
            - Adjacent empty cells are revealed if applicable
        Invariant:
            - Game state remains consistent
        
        Maps to: onClick() in original minesweeper.py
        """
        result = self.model.reveal_cell(x, y)
        self.view.update_cell(x, y)

        cell = self.model.board[x][y]
        if cell.adjacent_mines == 0:
            self.model.reveal_empty_cells(x, y, self.view.update_cell)

        if result == "LOSS":
            self.view.display_game_over(False)
        elif result == "WIN" or result == "WIN_TREASURE":
            self.view.display_game_over(result)

    def toggle_flag(self, x, y):
        """
        Handles toggling a flag on a cell.
        
        Precondition:
            - x and y must be valid board coordinates
            - Cell at (x,y) must not be revealed
        Postcondition:
            - Flag state is toggled
            - View is updated to reflect new flag state
            - Flag counter is updated
        Invariant:
            - Flag count remains consistent with board state
        
        Maps to: onRightClick() in original minesweeper.py
        """
        self.model.toggle_flag(x, y)
        self.view.update_cell(x, y)
        self.view.update_flags_label()

    def restart_game(self):
        """
        Restarts the game by resetting the model and refreshing the view.
        
        Precondition:
            - Model and view must be initialized
        Postcondition:
            - Game state is reset to initial conditions
            - Board is reinitialized based on mode
            - View is updated to reflect new game state
        Invariant:
            - Game configuration remains consistent with selected mode
        
        Maps to: restart() in original minesweeper.py
        """
        self.model.reset_game()
        if self.test_mode:
            self.model.initialize_test_board(self.test_board)
        else:
            self.model.initialize_board()
        self.model.start_time = None

        if hasattr(self.view, "setup_board"):
            self.view.setup_board()
            self.view.start_timer()
            self.view.labels["mines"].config(text=f"Mines: {self.model.mines_count}")
            self.view.update_flags_label()
        elif hasattr(self.view, "reset_view"):
            self.view.reset_view()

    def run(self):
        """
        Starts the main game loop.
        
        Precondition:
            - View must be properly initialized
            - Model must be in valid initial state
        Postcondition:
            - Game loop is started
            - View begins accepting user input
        Invariant:
            - Game state remains responsive to user input
        
        Maps to: main() and mainloop() in original minesweeper.py
        """
        self.view.run()