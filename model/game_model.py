import random
import logging

# Configure logging at the beginning of the file
logging.basicConfig(level=logging.DEBUG)

class GameModel:
    def __init__(self, rows, columns, num_mines):
        """
        Initializes the game model.
        :param rows: Number of rows in the game board
        :param columns: Number of columns in the game board
        :param num_mines: Number of mines to place on the board
        """
        self.rows = rows
        self.columns = columns
        self.num_mines = num_mines
        self.board = self._initialize_board()
        self.mine_positions = []
        self.game_over = False
        self.won = False
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, event_type, data=None):
        for observer in self.observers:
            observer.update(event_type, data)

    def _initialize_board(self):
        """
        Initializes an empty game board with all cells hidden.
        :return: 2D list representing the game board.
        """
        return [['H' for _ in range(self.columns)] for _ in range(self.rows)]

    def _place_mines(self, mine_positions=None):
        """
        Randomly place mines on the board.
        :return: List of mine positions.
        """
        if mine_positions:
            self.mine_positions = mine_positions
        else:
            mines = set()
            while len(mines) < self.num_mines:
                row = random.randint(0, self.rows - 1)
                column = random.randint(0, self.columns - 1)
                mines.add((row, column))
            self.mine_positions = list(mines)

        # Update the board with mines
        for (row, column) in self.mine_positions:
            if self.board[row][column] != 'M':
                self.board[row][column] = 'M'

        return self.mine_positions

    def reveal_cell(self, row, column):
        """
        Reveals the cell at the given position.
        :param row: Row index of the cell.
        :param column: Column index of the cell.
        :return: The value of the cell (e.g., mine, number, empty).
        """
        logging.debug(f"Attempting to reveal cell at ({row}, {column})")

        # Ensure the coordinates are within bounds
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            logging.debug("Out of bounds. Returning None.")
            return None

        # If the cell contains a mine, set game over and reveal the mine
        if self.board[row][column] == 'M':
            logging.debug(f"Mine found at ({row}, {column}). Setting game_over to True.")
            self.game_over = True
            self.notify_observers('game_over', {'row': row, 'column': column})
            return 'M'

        # Check if the cell is already revealed or flagged
        if self.board[row][column] not in ('H', 'F'):
            logging.debug(f"Cell already revealed or flagged. Current value: {self.board[row][column]}")
            return self.board[row][column]

        # Calculate the number of adjacent mines
        num_adjacent_mines = self._count_adjacent_mines(row, column)
        logging.debug(f"Number of adjacent mines at ({row}, {column}): {num_adjacent_mines}")

        if num_adjacent_mines > 0:
            # If there are adjacent mines, reveal the count
            self.board[row][column] = str(num_adjacent_mines)
            result = str(num_adjacent_mines)
        else:
            # If there are no adjacent mines, reveal as empty and recursively reveal neighbors
            self.board[row][column] = 'E'
            self._reveal_neighbors(row, column)
            result = 'E'
        
        # Notify observers of the change (e.g., UI update)
        self.notify_observers('cell_revealed', {'row': row, 'column': column, 'value': result})
        return result


        
    def _count_adjacent_mines(self, row, column):
        """
        Counts the number of mines adjacent to the given cell.
        :param row: Row index of the cell.
        :param column: Column index of the cell.
        :return: Number of adjacent mines.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, column + dc
            if 0 <= r < self.rows and 0 <= c < self.columns and (r, c) in self.mine_positions:
                count += 1
        return count
    
    def _reveal_neighbors(self, row, column):
        """
        Recursively reveals neighboring cells if they are empty.
        :param row: Row index of the current cell.
        :param column: Column index of the current cell.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, column + dc
            if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == 'H':
                self.reveal_cell(r, c)

    def flag_cell(self, row, column):
        """
        Flags or unflags a cell at the given position.
        :param row: Row index of the cell.
        :param column: Column index of the cell.
        """
        # Logic for placing or removing a flag.
        self.notify_observers('cell_flagged', {'row': row, 'column': column})
        pass

    def check_win_condition(self):
        """
        Checks if the player has won the game.
        :return: Boolean indicating if the game is won.
        """
        # Logic for checking if all non-mine cells are revealed.
        pass

    def get_board_state(self):
        """
        Returns the current state of the board.
        :return: 2D list representing the game board.
        """
        return self.board

    def add_hidden_treasure(self):
        """
        Adds a hidden treasure to a random empty cell.
        """
        # Logic for adding a hidden treasure to a cell.
        pass
