from model.game_model import GameModel
from controller.game_controller import GameController
from view.gui_view import GUIView
from view.text_view import TextView
from tkinter import Tk
from test_validator import TestValidator

def main():
    """
    Main function to initialize and start the Minesweeper game.
    Allows users to select the interface (GUI or text-based) and difficulty.
    """
    # Ask if user wants to enter testing mode
    print("Would you like to enter testing mode? (yes/no)")
    testing_mode = input().strip().lower() == 'yes'
    
    test_board = None
    if testing_mode:
        while test_board is None:
            print("Enter test board filename (CSV format):")
            filename = input().strip()
            test_board = TestValidator.read_test_board(filename)
            if test_board is None:
                print("Would you like to try another file? (yes/no)")
                if input().strip().lower() != 'yes':
                    testing_mode = False
                    break
            else:
                # Ask if user wants to play with this board
                print("Would you like to play with this board layout? (yes/no)")
                if input().strip().lower() != 'yes':
                    exit()
                # else:
                #     testing_mode = False
                #     test_board = None
        


    # Initialize model based on mode
    if testing_mode and test_board:
        game_model = GameModel(None)  # No difficulty needed for test board
        game_model.initialize_test_board(test_board)
    else:
        # Only ask for difficulty in normal game mode
        print("Select difficulty:")
        print("1. Beginner\t\t2. Intermediate\t\t3. Expert")
        difficulty_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'expert'
        }
        difficulty_level = input("Enter difficulty (1/2/3): ")
        if difficulty_level not in difficulty_map.keys():
            print('The level selected is not valid. Starting game in beginner mode.')
        difficulty = difficulty_map.get(difficulty_level, 'beginner')
        game_model = GameModel(difficulty)
        game_model.initialize_board()

     # Ask user for game mode
    print("Select game mode:")
    print("1. GUI")
    print("2. Text")
    mode = input("Enter mode (1/2): ")   

    # Create appropriate view and controller based on mode selection
    if mode == '1':
        # GUI Mode
        tk = Tk()
        tk.title("Minesweeper")
        gui_view = GUIView(tk, game_model, GameController(game_model, None, test_board, testing_mode))
        controller = GameController(game_model, gui_view, test_board, testing_mode)
        gui_view.controller = controller
        tk.mainloop()
    elif mode == '2':
        # Text-based Mode
        controller = GameController(game_model, None, test_board, testing_mode)
        text_view = TextView(game_model, controller)
        controller.view = text_view
        text_view.run()
    else:
        print("Invalid mode! Exiting game.")
        exit()



if __name__ == "__main__":
    main()