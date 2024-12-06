import csv

class TestValidator:
    """Handles validation of test board files for Minesweeper."""

    def validate_test_board(self, board):
        """
        Validates test board according to requirements and provides specific feedback.

        :param board: 2D list representing the board.
        :return: True if the board is valid, False otherwise.
        """
        try:
            # Validate the board
            is_valid, board_data = self.validate_board(board)
            if not is_valid:
                print("Board does not meet test criteria.")
                return False

            print("Board validation successful!")
            return True

        except Exception as e:
            print(f"Error validating test board: {e}")
            return False

    def validate_board(self, board_data):
        """
        Validates the board data against the given rules.

        :param board_data: 2D list representing the board.
        :return: Tuple (is_valid, board_data) where is_valid is True if valid,
                 and board_data is the parsed board data if valid.
        """
        # Check board dimensions
        if len(board_data) != 8 or any(len(row) != 8 for row in board_data):
            print("Invalid board dimensions. Board must be 8x8.")
            return False, None

        mine_positions = []
        treasure_count = 0

        # Iterate through the board to collect mines and treasures
        for x, row in enumerate(board_data):
            for y, value in enumerate(row):
                if value == 1:  # Mine
                    mine_positions.append((x, y))
                elif value == 2:  # Treasure
                    treasure_count += 1
                elif value != 0:  # Invalid value
                    print(f"Invalid value {value} at ({x}, {y}). Must be 0, 1, or 2.")
                    return False, None

        # Validate treasures
        if treasure_count > 9:
            print("Invalid number of treasures. Must be no more than 9.")
            return False, None

        # Validate mine positions
        if not self.validate_mine_positions(mine_positions):
            return False, None

        return True, board_data

    def validate_mine_positions(self, mine_positions):
        """
        Validates the placement of mines according to the specified rules.

        :param mine_positions: List of (x, y) positions for mines.
        :return: True if the mine placement is valid, False otherwise.
        """
        if len(mine_positions) != 10:
            print(f"Error: Board must have exactly 10 mines. Found {len(mine_positions)} mines.")
            return False

        # Ensure there are at least 8 mines
        if len(mine_positions) < 8:
            print("Insufficient mines. There must be at least 8 mines.")
            return False

        # Select the first 8 mines with unique rows and columns
        first_eight_mines = []
        rows = set()
        cols = set()
        diagonal_found = False

        for x, y in mine_positions:
            if x not in rows and y not in cols:
                first_eight_mines.append((x, y))
                rows.add(x)
                cols.add(y)
                if x == y:  # Check for a diagonal mine
                    diagonal_found = True
                if len(first_eight_mines) == 8:
                    break

        # If a diagonal mine is not found, replace the last mine with a diagonal one if possible
        if not diagonal_found:
            for x, y in mine_positions:
                if x == y and (x, y) not in first_eight_mines:
                    first_eight_mines[-1] = (x, y)
                    diagonal_found = True
                    break

        # Validate the selection of the first 8 mines
        if len(first_eight_mines) < 8 or not diagonal_found:
            print("Error: Unable to select 8 mines with unique rows and columns, with one on the diagonal.")
            return False

        # Ensure none of the first 8 mines are adjacent by row or column
        for i, (x1, y1) in enumerate(first_eight_mines):
            for j, (x2, y2) in enumerate(first_eight_mines):
                if i != j and (
                    (abs(x1 - x2) == 1 and y1 == y2) or (x1 == x2 and abs(y1 - y2) == 1)
                ):
                    print(f"Mine placement error: ({x1}, {y1}) is adjacent to ({x2}, {y2}) by row or column.")
                    return False

        # Identify remaining mines
        remaining_mines = [mine for mine in mine_positions if mine not in first_eight_mines]

        # Iterate to find a valid 9th and 10th mine combination
        for ninth_mine in remaining_mines:
            x9, y9 = ninth_mine

            # Check adjacency of the 9th mine to any of the first 8 mines by row or column
            adjacent_to_first_eight = any(
                (abs(x9 - x) == 1 and y9 == y) or (x9 == x and abs(y9 - y) == 1)
                for x, y in first_eight_mines
            )

            if not adjacent_to_first_eight:
                continue  # Skip this mine as it can't be the 9th

            # Check for a valid 10th mine that is isolated
            for tenth_mine in remaining_mines:
                if tenth_mine == ninth_mine:
                    continue  # Skip the 9th mine itself

                x10, y10 = tenth_mine
                is_isolated = not any(
                    (abs(x10 - x) <= 1 and abs(y10 - y) <= 1)
                    for x, y in first_eight_mines + [ninth_mine]
                )

                if is_isolated:
                    # Found a valid combination for 9th and 10th mines
                    return True

        # If no valid combination is found
        print("Unable to find a valid 9th and 10th mine combination.")
        return False

    @staticmethod
    def read_test_board(filename):
        """Reads and validates a test board from a CSV file.

        :param filename: Path to the CSV file containing the board layout.
        :return: 2D list representing the board if valid, None otherwise.
        """
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                board = [[int(cell) for cell in row] for row in reader]

            # Check board dimensions
            if len(board) != 8 or any(len(row) != 8 for row in board):
                print("Invalid board dimensions. Must be 8x8.")
                return None

            # Validate the board
            validator = TestValidator()
            if not validator.validate_test_board(board):
                print("Board does not meet test criteria.")
                return None

            return board
        except Exception as e:
            print(f"Error reading test board: {e}")
            return None
