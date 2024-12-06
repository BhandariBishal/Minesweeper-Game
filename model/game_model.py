from random import sample, randint
from datetime import datetime


class Cell:
    """
    Represents a single cell on the Minesweeper board.
    Contains information about:
    - Mine presence
    - Flag status
    - Revealed status
    - Adjacent mine count
    - Treasure presence
    - Position coordinates
    
    Invariants:
        - A cell cannot be both revealed and flagged
        - A cell cannot be both a mine and a treasure
        - Adjacent mines count must be between 0 and 8
        - Coordinates must be non-negative when set
    """
    def __init__(self, is_mine=False, has_treasure=False, x=None, y=None):
        """
        Initializes a new cell with specified properties.
        
        Precondition:
            - x and y must be None or non-negative integers
            - is_mine and has_treasure cannot both be True
        Postcondition:
            - Cell is initialized with default state (not revealed, not flagged)
            - Mine and treasure status are set as specified
            - Coordinates are set if provided
        Invariant:
            - Cell maintains valid state combinations
        
        Maps to: setup() tile initialization in original minesweeper.py
        """
        self.is_mine = is_mine
        self.is_flagged = False
        self.is_revealed = False
        self.adjacent_mines = 0
        self.has_treasure = has_treasure
        self.x = x
        self.y = y

    def reveal(self):
        """
        Marks the cell as revealed if not flagged.
        
        Precondition:
            - Cell must be initialized
        Postcondition:
            - Cell is revealed if not flagged
            - No change if cell is flagged
        Invariant:
            - Flagged cells cannot be revealed
            - Revealed state cannot be reversed
        
        Maps to: onClick() tile state change in original minesweeper.py
        """
        if not self.is_flagged:
            self.is_revealed = True

    def toggle_flag(self):
        """
        Toggles the flag state of the cell if not revealed.
        
        Precondition:
            - Cell must be initialized
            - Cell must not be revealed
        Postcondition:
            - Flag state is toggled if cell is not revealed
            - No change if cell is revealed
        Invariant:
            - Revealed cells cannot be flagged
            - Flag state can only be True or False
        
        Maps to: onRightClick() flag toggling in original minesweeper.py
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

class GameModel:
    """
    Implements the core game logic for Minesweeper.
    Handles board initialization, game state, and win conditions.
    """
    DIFFICULTY_TO_LEVEL = {
        'beginner': {
            'board_size': (8, 8),
            'mines_range': (1, 10)
        },
        'intermediate': {
            'board_size': (16, 16),
            'mines_range': (11, 40)
        },
        'expert': {
            'board_size': (30, 16),
            'mines_range': (41, 99)
        }
    }

    def __init__(self, difficulty):
        """
        Initializes a new game with specified difficulty.
        
        Precondition:
            - difficulty must be one of: 'beginner', 'intermediate', 'expert'
        Postcondition:
            - Game board is empty
            - All counters are initialized to 0
            - Difficulty settings are applied
        Invariant:
            - Board size matches difficulty specifications
        
        Maps to: __init__ and setup() in original minesweeper.py
        """
        self.board = []
        self.difficulty = self.DIFFICULTY_TO_LEVEL.get(difficulty)
        if not self.difficulty:
            raise ValueError(f"Unknown difficulty level: {difficulty}")
        self.mines_count = 0
        self.flags_count = 0
        self.board_size = (0, 0)
        self.start_time = None
        self.clicked_count = 0

    def initialize_test_board(self, test_board):
        """
        Initializes the game board using a test board configuration.
        
        Precondition:
            - test_board must be a 2D list of integers (0, 1, or 2)
            - test_board must be rectangular
        Postcondition:
            - Board is initialized with test configuration
            - Mine and treasure positions are set
            - Adjacent mine counts are calculated
        Invariant:
            - Board dimensions remain constant
        
        Maps to: setup() in original minesweeper.py
        """
        rows = len(test_board)
        cols = len(test_board[0])
        self.board_size = (rows, cols)
        self.board = [[Cell(x=i, y=j) for j in range(cols)] for i in range(rows)]
        
        self.mines_count = 0
        for i in range(rows):
            for j in range(cols):
                if test_board[i][j] == 1:
                    self.board[i][j].is_mine = True
                    self.mines_count += 1
                elif test_board[i][j] == 2:
                    self.board[i][j].has_treasure = True
        
        for x in range(rows):
            for y in range(cols):
                self.board[x][y].adjacent_mines = self._calculate_adjacent_mines(x, y)

    def initialize_board(self):
        """
        Creates and initializes the game board with mines and treasures.
        
        Precondition:
            - Difficulty settings must be valid
            - Board must be empty
        Postcondition:
            - Board is populated with mines and treasures
            - Adjacent mine counts are calculated
        Invariant:
            - Number of mines is within difficulty range
            - Number of treasures is less than number of mines
        
        Maps to: setup() in original minesweeper.py
        """
        row, col = self.difficulty['board_size']
        self.board_size = self.difficulty['board_size']
        self.board = [[Cell(x=i, y=j) for j in range(col)] for i in range(row)]
        self.mines_count = randint(*self.difficulty['mines_range'])
        num_mines = self.mines_count

        mine_positions = sample(range(row * col), num_mines)
        for pos in mine_positions:
            x, y = divmod(pos, col)
            self.board[x][y].is_mine = True

        if num_mines > 1:
            treasures_count = randint(0, num_mines - 1)
        else:
            treasures_count = 0

        available_positions = [pos for pos in range(row * col) if pos not in mine_positions]
        if treasures_count > 0:
            treasure_positions = sample(available_positions, treasures_count)
            for pos in treasure_positions:
                x, y = divmod(pos, col)
                self.board[x][y].has_treasure = True

        for x in range(row):
            for y in range(col):
                self.board[x][y].adjacent_mines = self._calculate_adjacent_mines(x, y)

    def _calculate_adjacent_mines(self, x, y):
        """
        Calculates the number of adjacent mines for a cell.
        
        Precondition:
            - x and y must be valid board coordinates
            - Board must be initialized
        Postcondition:
            - Returns count of adjacent mines (0-8)
        Invariant:
            - Count cannot exceed 8
            - Count cannot be negative
        
        Maps to: getNeighbors() mine counting in original minesweeper.py
        """
        count = 0
        for neighbor in self.get_neighbors(x, y):
            if neighbor.is_mine:
                count += 1
        return count

    def get_neighbors(self, x, y):
        """
        Returns a list of neighboring cells for given coordinates.
        
        Precondition:
            - x and y must be valid board coordinates
            - Board must be initialized
        Postcondition:
            - Returns list of valid neighboring Cell objects
        Invariant:
            - Number of neighbors ≤ 8
            - All returned cells are valid board positions
        
        Maps to: getNeighbors() in original minesweeper.py
        """
        rows, cols = self.board_size
        neighbors = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), 
                       (0, -1),          (0, 1), 
                       (1, -1),  (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append(self.board[nx][ny])
        return neighbors

    def reveal_cell(self, x, y):
        """
        Reveals a cell and handles game state changes.
        
        Precondition:
            - x and y must be valid board coordinates
            - Board must be initialized
        Postcondition:
            - Cell is revealed if not flagged
            - Game state is updated based on reveal result
        Invariant:
            - Game state remains valid
            - Clicked count only increases for valid reveals
        
        Maps to: onClick() in original minesweeper.py
        """
        if self.start_time is None:
            self.start_time = datetime.now()

        cell = self.board[x][y]
        if cell.is_revealed or cell.is_flagged:
            return False

        cell.reveal()
        self.clicked_count += 1

        if cell.has_treasure:
            return "WIN_TREASURE"

        if cell.is_mine:
            return "LOSS"

        return self.check_win_condition()

    def reveal_empty_cells(self, x, y, update_view):
        """
        Reveals empty cells recursively and updates the view.
        
        Precondition:
            - x and y must be valid board coordinates
            - update_view must be a valid callback function
        Postcondition:
            - All connected empty cells are revealed
            - View is updated for each revealed cell
        Invariant:
            - Treasures remain hidden
            - Flagged cells remain unchanged
        
        Maps to: clearSurroundingTiles() in original minesweeper.py
        """
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            for neighbor in self.get_neighbors(cx, cy):
                if not neighbor.is_revealed and not neighbor.is_flagged and not neighbor.has_treasure:
                    neighbor.reveal()
                    update_view(neighbor.x, neighbor.y)
                    if neighbor.adjacent_mines == 0:
                        stack.append((neighbor.x, neighbor.y))

    def toggle_flag(self, x, y):
        """
        Toggles flag state of a cell and updates flag count.
        
        Precondition:
            - x and y must be valid board coordinates
            - Board must be initialized
        Postcondition:
            - Cell flag state is toggled if not revealed
            - Flag count is updated accordingly
        Invariant:
            - Flag count matches number of flagged cells
            - Revealed cells cannot be flagged
        
        Maps to: onRightClick() in original minesweeper.py
        """
        cell = self.board[x][y]
        if not cell.is_revealed:
            cell.toggle_flag()
            self.flags_count += 1 if cell.is_flagged else -1

    def check_win_condition(self):
        """
        Checks if the game has been won through regular means.
        
        Precondition:
            - Board must be initialized
            - Game must be in progress
        Postcondition:
            - Returns "WIN" if won, False otherwise
        Invariant:
            - Win condition remains consistent with game rules
            - Incorrect flags prevent win condition
        
        Maps to: gameOver() win condition check in original minesweeper.py
        """
        unrevealed_count = 0
        flagged_mines = 0

        for row in self.board:
            for cell in row:
                if not cell.is_revealed:
                    unrevealed_count += 1
                if cell.is_mine and cell.is_flagged:
                    flagged_mines += 1
                if not cell.is_mine and cell.is_flagged:
                    return False
        
        if unrevealed_count == self.mines_count or flagged_mines == self.mines_count:
            return "WIN"
        
        if all(cell.is_revealed or cell.is_mine for row in self.board for cell in row):
            return "WIN"

        return False

    def reset_game(self):
        """
        Resets the game state for a new game.
        
        Precondition:
            - Game model must exist
        Postcondition:
            - All game state variables reset to initial values
            - Board cleared and ready for new game
        Invariant:
            - All counters are non-negative
            - Board size matches difficulty settings
        
        Maps to: restart() in original minesweeper.py
        """
        self.board = []
        self.mines_count = 0
        self.flags_count = 0
        self.board_size = (0, 0)
        self.start_time = None
        self.clicked_count = 0
