import logging
from model.game_model import GameModel

logging.basicConfig(level=logging.DEBUG)

# Simple Test for the Constructor
def test_constructor():
    # Test parameters
    rows = 8
    columns = 8
    num_mines = 10

    # Instantiate the GameModel
    game_model = GameModel(rows, columns, num_mines)

    # Check the dimensions of the board
    assert len(game_model.board) == rows, f"Expected {rows} rows, but got {len(game_model.board)}"
    assert len(game_model.board[0]) == columns, f"Expected {columns} columns, but got {len(game_model.board[0])}"

    # Check that each cell is initialized as 'H' (hidden)
    for row in game_model.board:
        for cell in row:
            assert cell == 'H', f"Expected 'H' for each cell, but got {cell}"

    # Check other attributes
    assert game_model.num_mines == num_mines, f"Expected {num_mines} mines, but got {game_model.num_mines}"
    assert game_model.mine_positions == [], "Expected empty mine positions list"
    assert game_model.game_over == False, "Expected game_over to be False"
    assert game_model.won == False, "Expected won to be False"

    print("test_constructor passed.")

def test_place_mines():
    # Test parameters
    rows = 8
    columns = 8
    num_mines = 10

    # Instantiate the GameModel
    game_model = GameModel(rows, columns, num_mines)

    # Place the mines
    mine_positions = game_model._place_mines()

    # Check the number of mines placed
    assert len(mine_positions) == num_mines, f"Expected {num_mines} mines, but got {len(mine_positions)}"

    # Check that all positions are unique
    assert len(set(mine_positions)) == num_mines, "Expected unique mine positions"

    # Verify that the mine positions are marked correctly on the board
    for (row, column) in mine_positions:
        assert game_model.board[row][column] == 'M', f"Expected 'M' at ({row}, {column})"

    print("test_place_mines passed.")

def test_reveal_cell():
    # Test parameters
    rows = 4
    columns = 4
    num_mines = 2

    # Instantiate the GameModel
    game_model = GameModel(rows, columns, num_mines)

    # Place mines for testing purposes away from (0, 0)
    mine_positions = [(3, 3), (2, 1)]
    game_model._place_mines(mine_positions)

    logging.debug(f"Mine positions: {game_model.mine_positions}")
    logging.debug("Initial board state:")
    for row in game_model.board:
        logging.debug(row)

    # Reveal a cell that is not a mine and not adjacent to any mines
    logging.debug("Revealing cell at (0, 0)...")
    result = game_model.reveal_cell(0, 0)
    assert result == 'E', f"Expected 'E' for an empty cell, but got {result}"
    assert game_model.board[0][0] == 'E', f"Expected 'E' at (0, 0), but got {game_model.board[0][0]}"

    # Reveal a cell adjacent to a mine
    logging.debug("Revealing cell at (2, 0)...")
    result = game_model.reveal_cell(2, 0)
    assert result == '1', f"Expected '1' for a cell adjacent to one mine, but got {result}"
    assert game_model.board[2][0] == '1', f"Expected '1' at (2, 0), but got {game_model.board[2][0]}"

    # Reveal a cell that is a mine (should trigger game over)
    logging.debug("Revealing cell at (3, 3)...")
    result = game_model.reveal_cell(3, 3)
    assert result == 'M', f"Expected 'M' for a mine cell, but got {result}"
    assert game_model.game_over == True, "Expected game_over to be True after revealing a mine"
    logging.debug(f"Test reveal mine at (3, 3): game_over = {game_model.game_over}")

    print("test_reveal_cell passed.")


def test_flag_cell():
    # Test parameters
    rows = 4
    cols = 4
    num_mines = 2

    # Instantiate the GameModel
    game_model = GameModel(rows, cols, num_mines)

    # Place a flag on a cell that is hidden
    result = game_model.flag_cell(0, 0)
    assert result == 'F', f"Expected 'F' for a flagged cell, but got {result}"
    assert game_model.board[0][0] == 'F', f"Expected 'F' at (0, 0), but got {game_model.board[0][0]}"
    logging.debug(f"Flagged cell at (0, 0): {game_model.board[0][0]}")

    # Remove the flag from the same cell
    result = game_model.flag_cell(0, 0)
    assert result == 'H', f"Expected 'H' for an unflagged cell, but got {result}"
    assert game_model.board[0][0] == 'H', f"Expected 'H' at (0, 0), but got {game_model.board[0][0]}"
    logging.debug(f"Unflagged cell at (0, 0): {game_model.board[0][0]}")

    # Try to flag a revealed cell (manually reveal it first)
    game_model.reveal_cell(1, 1)
    result = game_model.flag_cell(1, 1)
    assert result == 'E', f"Expected 'E' for a revealed cell, but got {result}"
    assert game_model.board[1][1] == 'E', f"Expected 'E' at (1, 1), but got {game_model.board[1][1]}"
    logging.debug(f"Tried flagging revealed cell at (1, 1): {game_model.board[1][1]}")

    print("test_flag_cell passed.")


def test_check_win_condition():
    # Test parameters
    rows = 4
    cols = 4
    num_mines = 2

    # Instantiate the GameModel
    game_model = GameModel(rows, cols, num_mines)

    # Place mines for testing purposes at specific positions
    mine_positions = [(3, 3), (2, 1)]
    game_model._place_mines(mine_positions)

    # Reveal all non-mine cells to simulate a win
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in mine_positions:
                game_model.reveal_cell(row, col)

    # Check if the win condition is correctly set to True
    result = game_model.check_win_condition()
    assert result == True, "Expected win condition to be True, but got False."
    assert game_model.won == True, "Expected won attribute to be True after all non-mine cells are revealed."
    logging.debug("Win condition verified successfully.")

    print("test_check_win_condition passed.")

def test_reset_game():
    # Test parameters
    rows = 4
    cols = 4
    num_mines = 2

    # Instantiate the GameModel
    game_model = GameModel(rows, cols, num_mines)

    # Place mines for testing purposes
    mine_positions = [(3, 3), (2, 1)]
    game_model._place_mines(mine_positions)

    # Reveal some cells
    game_model.reveal_cell(0, 0)
    game_model.reveal_cell(1, 1)
    
    # Flag a cell
    game_model.flag_cell(0, 1)

    # Check the state before reset
    assert game_model.board[0][0] != 'H', "Expected cell (0, 0) to be revealed."
    assert game_model.board[0][1] == 'F', "Expected cell (0, 1) to be flagged."

    # Reset the game
    game_model.reset_game()

    # Check the state after reset: All cells should be hidden ('H')
    for row in range(rows):
        for col in range(cols):
            assert game_model.board[row][col] == 'H', f"Expected all cells to be hidden after reset, but got {game_model.board[row][col]} at ({row}, {col})"

    # Check that the mine positions are reset (new positions are generated)
    assert len(game_model.mine_positions) == num_mines, "Expected new mine positions after reset."

    # Check that game_over and won are reset
    assert game_model.game_over == False, "Expected game_over to be False after reset."
    assert game_model.won == False, "Expected won to be False after reset."

    logging.debug("Game successfully reset and verified.")

    print("test_reset_game passed.")



# Run the tests
if __name__ == "__main__":
    test_constructor()
    test_place_mines()
    test_reveal_cell()
    test_flag_cell()
    test_check_win_condition()
    test_reset_game()


