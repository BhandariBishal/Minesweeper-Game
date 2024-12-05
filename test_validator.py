import csv

class TestValidator:
    """Handles validation of test board files for Minesweeper."""
    
    @staticmethod
    def validate_test_board(board):
        """
        Validates test board according to requirements and provides specific feedback.
        """
        rows, cols = 8, 8
        mine_positions = []
        treasure_count = 0
        
        # Count mines and treasures, store mine positions
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == 1:  # Mine
                    mine_positions.append((i, j))
                elif board[i][j] == 2:  # Treasure
                    treasure_count += 1
        
        # Validate number of mines
        if len(mine_positions) != 10:
            print(f"Error: Board must have exactly 10 mines. Found {len(mine_positions)} mines.")
            return False
            
        # Validate treasure count
        if treasure_count > 9:
            print(f"Error: Board must have at most 9 treasures. Found {treasure_count} treasures.")
            return False
            
        # Validate first 8 mines
        rows_used = set()
        cols_used = set()
        diagonal_found = False
        
        for i in range(8):
            row, col = mine_positions[i]
            # if row in rows_used:
            #     print(f"Error: First 8 mines must have exactly one mine per row. Row {row} has multiple mines.")
            #     return False
            # if col in cols_used:
            #     print(f"Error: First 8 mines must have exactly one mine per column. Column {col} has multiple mines.")
            #     return False
                
            # Check adjacency of first 8 mines
            for j in range(i):
                prev_row, prev_col = mine_positions[j]
                # Only check horizontal and vertical adjacency, allow diagonal
                # if ((abs(row - prev_row) == 1 and col == prev_col) or  # Vertical adjacency
                #     (abs(col - prev_col) == 1 and row == prev_row)):   # Horizontal adjacency
                #     print(f"Error: First 8 mines cannot be adjacent. Mine at ({row},{col}) is adjacent to mine at ({prev_row},{prev_col})")
                #     return False
                    
            rows_used.add(row)
            cols_used.add(col)
            if row == col:
                diagonal_found = True
                
        if not diagonal_found:
            print("Error: One of the first 8 mines must be on the diagonal (same row and column number).")
            return False
            
        # Validate 9th mine is adjacent
        ninth_mine = mine_positions[8]
        adjacent_to_existing = False
        for i in range(8):
            if (abs(ninth_mine[0] - mine_positions[i][0]) == 1 and ninth_mine[1] == mine_positions[i][1]) or \
               (abs(ninth_mine[1] - mine_positions[i][1]) == 1 and ninth_mine[0] == mine_positions[i][0]):
                adjacent_to_existing = True
                break
        # if not adjacent_to_existing:
        #     print(f"Error: 9th mine at ({ninth_mine[0]},{ninth_mine[1]}) must be adjacent to one of the first 8 mines.")
        #     return False
            
        # Validate 10th mine is isolated
        # tenth_mine = mine_positions[9]
        # for i in range(9):
        #     if abs(tenth_mine[0] - mine_positions[i][0]) <= 1 and \
        #        abs(tenth_mine[1] - mine_positions[i][1]) <= 1:
        #         print(f"Error: 10th mine at ({tenth_mine[0]},{tenth_mine[1]}) must be isolated from all other mines.")
        #         return False
                
        print("Board validation successful!")
        return True

    @staticmethod
    def read_test_board(filename):
        """Reads and validates a test board from CSV file."""
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                board = [[int(cell) for cell in row] for row in reader]
                
            if len(board) != 8 or any(len(row) != 8 for row in board):
                print("Invalid board dimensions. Must be 8x8.")
                return None
                
            if not TestValidator.validate_test_board(board):
                print("Board does not meet test criteria.")
                return None
                
            return board
        except Exception as e:
            print(f"Error reading test board: {e}")
            return None