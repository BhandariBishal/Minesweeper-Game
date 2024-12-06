import csv

class TestValidator:
    """
    Handles validation of test board files for Minesweeper.
    
    Invariants:
        - All validation methods must maintain consistent error reporting
        - Board dimensions must remain 8x8 throughout validation
    """

    def validate_test_board(self, board):
        """
        Validates test board according to requirements and provides specific feedback.
        
        Precondition:
            - board must be a 2D list
            - board must contain only integers
        Postcondition:
            - Returns True only if board meets all validation criteria
            - Provides appropriate error messages for invalid boards
        Invariant:
            - Validation rules remain consistent throughout execution
        
        Maps to: setup() board validation in original minesweeper.py
        """
        try:
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
        
        Precondition:
            - board_data must be a 2D list
            - board_data must contain only integers (0, 1, or 2)
        Postcondition:
            - Returns (True, board_data) if valid
            - Returns (False, None) if invalid with appropriate error message
        Invariant:
            - Validation criteria remain constant
            - Board structure remains unchanged during validation
        
        Maps to: setup() board initialization in original minesweeper.py
        """
        if len(board_data) != 8 or any(len(row) != 8 for row in board_data):
            print("Invalid board dimensions. Board must be 8x8.")
            return False, None

        mine_positions = []
        treasure_count = 0

        for x, row in enumerate(board_data):
            for y, value in enumerate(row):
                if value == 1:
                    mine_positions.append((x, y))
                elif value == 2:
                    treasure_count += 1
                elif value != 0:
                    print(f"Invalid value {value} at ({x}, {y}). Must be 0, 1, or 2.")
                    return False, None

        if treasure_count > 9:
            print("Invalid number of treasures. Must be no more than 9.")
            return False, None

        if not self.validate_mine_positions(mine_positions):
            return False, None

        return True, board_data

    def validate_mine_positions(self, mine_positions):
        """
        Validates the placement of mines according to the specified rules.
        
        Precondition:
            - mine_positions must be a list of (x,y) tuples
            - All coordinates must be within 8x8 board
        Postcondition:
            - Returns True only if mine placement meets all rules
            - Provides specific error messages for invalid placements
        Invariant:
            - Mine placement rules remain consistent
            - Original mine positions list remains unchanged
        
        Maps to: setup() mine placement validation in original minesweeper.py
        """
        if len(mine_positions) != 10:
            print(f"Error: Board must have exactly 10 mines. Found {len(mine_positions)} mines.")
            return False

        if len(mine_positions) < 8:
            print("Insufficient mines. There must be at least 8 mines.")
            return False

        first_eight_mines = []
        rows = set()
        cols = set()
        diagonal_found = False

        for x, y in mine_positions:
            if x not in rows and y not in cols:
                first_eight_mines.append((x, y))
                rows.add(x)
                cols.add(y)
                if x == y:
                    diagonal_found = True
                if len(first_eight_mines) == 8:
                    break

        if not diagonal_found:
            for x, y in mine_positions:
                if x == y and (x, y) not in first_eight_mines:
                    first_eight_mines[-1] = (x, y)
                    diagonal_found = True
                    break

        if len(first_eight_mines) < 8 or not diagonal_found:
            print("Error: Unable to select 8 mines with unique rows and columns, with one on the diagonal.")
            return False

        for i, (x1, y1) in enumerate(first_eight_mines):
            for j, (x2, y2) in enumerate(first_eight_mines):
                if i != j and (
                    (abs(x1 - x2) == 1 and y1 == y2) or (x1 == x2 and abs(y1 - y2) == 1)
                ):
                    print(f"Mine placement error: ({x1}, {y1}) is adjacent to ({x2}, {y2}) by row or column.")
                    return False

        remaining_mines = [mine for mine in mine_positions if mine not in first_eight_mines]

        for ninth_mine in remaining_mines:
            x9, y9 = ninth_mine

            adjacent_to_first_eight = any(
                (abs(x9 - x) == 1 and y9 == y) or (x9 == x and abs(y9 - y) == 1)
                for x, y in first_eight_mines
            )

            if not adjacent_to_first_eight:
                continue

            for tenth_mine in remaining_mines:
                if tenth_mine == ninth_mine:
                    continue

                x10, y10 = tenth_mine
                is_isolated = not any(
                    (abs(x10 - x) <= 1 and abs(y10 - y) <= 1)
                    for x, y in first_eight_mines + [ninth_mine]
                )

                if is_isolated:
                    return True

        print("Unable to find a valid 9th and 10th mine combination.")
        return False

    @staticmethod
    def read_test_board(filename):
        """
        Reads and validates a test board from a CSV file.
        
        Precondition:
            - filename must be a string
            - File must exist and be readable
            - File must contain valid CSV data
        Postcondition:
            - Returns valid 8x8 board as 2D list if successful
            - Returns None with error message if invalid
        Invariant:
            - File contents remain unchanged
            - CSV parsing rules remain consistent
        
        Maps to: setup() board initialization in original minesweeper.py
        """
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                board = [[int(cell) for cell in row] for row in reader]

            if len(board) != 8 or any(len(row) != 8 for row in board):
                print("Invalid board dimensions. Must be 8x8.")
                return None

            validator = TestValidator()
            if not validator.validate_test_board(board):
                print("Board does not meet test criteria.")
                return None

            return board
        except Exception as e:
            print(f"Error reading test board: {e}")
            return None