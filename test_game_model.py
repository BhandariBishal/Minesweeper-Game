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




# Run the test
if __name__ == "__main__":

    test_constructor()
    test_place_mines()
    test_reveal_cell()
