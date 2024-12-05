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
    """
    def __init__(self, is_mine=False, has_treasure=False, x=None, y=None):
        self.is_mine = is_mine
        self.is_flagged = False
        self.is_revealed = False
        self.adjacent_mines = 0
        self.has_treasure = has_treasure  # New: treasure attribute for instant win condition
        self.x = x  # Row index
        self.y = y  # Column index

    def reveal(self):
        """Marks the cell as revealed if not flagged."""
        if not self.is_flagged:
            self.is_revealed = True

    def toggle_flag(self):
        """Toggles the flag state of the cell if not revealed."""
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
            'mines_range': (1, 10),
            'treasures': 2  # New: treasure count for beginner level
        },
        'intermediate': {
            'board_size': (16, 16),
            'mines_range': (11, 40),
            'treasures': 4  # New: treasure count for intermediate level
        },
        'expert': {
            'board_size': (30, 16),
            'mines_range': (41, 99),
            'treasures': 6  # New: treasure count for expert level
        }
    }

    def __init__(self, difficulty):
        """
        Initializes a new game with specified difficulty.
        """
        self.board = []
        self.difficulty = self.DIFFICULTY_TO_LEVEL.get(difficulty)
        self.mines_count = 0
        self.flags_count = 0
        self.board_size = (0, 0)
        self.start_time = None
        self.clicked_count = 0

    def initialize_test_board(self, test_board):
        """
        Initializes the game board using a test board configuration from CSV.
        Args:
            test_board: 2D list containing the test board layout where:
                0 = empty cell
                1 = mine
                2 = treasure
        """
        rows = len(test_board)
        cols = len(test_board[0])
        self.board_size = (rows, cols)
        self.board = [[Cell(x=i, y=j) for j in range(cols)] for i in range(rows)]
        
        # Place mines and treasures according to test board
        self.mines_count = 0
        for i in range(rows):
            for j in range(cols):
                if test_board[i][j] == 1:  # Mine
                    self.board[i][j].is_mine = True
                    self.mines_count += 1
                elif test_board[i][j] == 2:  # Treasure
                    self.board[i][j].has_treasure = True
        
        # Calculate adjacent mines for each cell
        for x in range(rows):
            for y in range(cols):
                self.board[x][y].adjacent_mines = self._calculate_adjacent_mines(x, y)

    def initialize_board(self):
        """
        Creates and initializes the game board with mines and treasures.
        Calculates adjacent mine counts for each cell.
        """
        row, col = self.difficulty['board_size']
        self.board_size = self.difficulty['board_size']
        self.board = [[Cell(x=i, y=j) for j in range(col)] for i in range(row)]
        self.mines_count = randint(*self.difficulty['mines_range'])
        num_mines = self.mines_count

        # Randomly place mines
        mine_positions = sample(range(row * col), num_mines)
        for pos in mine_positions:
            x, y = divmod(pos, col)
            self.board[x][y].is_mine = True

        # New: Place treasures in non-mine positions
        treasure_positions = sample(
            [pos for pos in range(row * col) if pos not in mine_positions],
            self.difficulty['treasures']
        )
        for pos in treasure_positions:
            x, y = divmod(pos, col)
            self.board[x][y].has_treasure = True

        # Calculate adjacent mines for each cell
        for x in range(row):
            for y in range(col):
                self.board[x][y].adjacent_mines = self._calculate_adjacent_mines(x, y)

    def _calculate_adjacent_mines(self, x, y):
        """Calculates the number of adjacent mines for a cell."""
        count = 0
        for neighbor in self.get_neighbors(x, y):
            if neighbor.is_mine:
                count += 1
        return count

    def get_neighbors(self, x, y):
        """Returns a list of neighboring cells for given coordinates."""
        rows, cols = self.board_size
        neighbors = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append(self.board[nx][ny])
        return neighbors

    def reveal_cell(self, x, y):
        """
        Reveals a cell and handles game state changes.
        Returns:
        - "WIN_TREASURE" if treasure is found
        - "LOSS" if mine is revealed
        - Result of check_win_condition() otherwise
        """
        if self.start_time is None:
            self.start_time = datetime.now()

        cell = self.board[x][y]
        if cell.is_revealed or cell.is_flagged:
            return False

        cell.reveal()
        self.clicked_count += 1

        # New: Check for treasure win condition first
        if cell.has_treasure:
            return "WIN_TREASURE"

        if cell.is_mine:
            return "LOSS"

        return self.check_win_condition()

    def reveal_empty_cells(self, x, y, update_view):
        """
        Reveals empty cells recursively and updates the view.
        Treasures should not be revealed during this process.
        """
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            for neighbor in self.get_neighbors(cx, cy):
                # Don't reveal treasures during flood fill
                if not neighbor.is_revealed and not neighbor.is_flagged and not neighbor.has_treasure:
                    neighbor.reveal()
                    update_view(neighbor.x, neighbor.y)
                    if neighbor.adjacent_mines == 0:
                        stack.append((neighbor.x, neighbor.y))

    def toggle_flag(self, x, y):
        """Toggles flag state of a cell and updates flag count."""
        cell = self.board[x][y]
        if not cell.is_revealed:
            cell.toggle_flag()
            self.flags_count += 1 if cell.is_flagged else -1

    def check_win_condition(self):
        """
        Checks if the game has been won through regular means:
        - All non-mine cells revealed
        - All mines correctly flagged
        Returns "WIN" if won, False otherwise
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
        """Resets the game state for a new game."""
        self.board = []
        self.mines_count = 0
        self.flags_count = 0
        self.board_size = (0, 0)
        self.start_time = None
        
      