class TextView:
    """
    Text-based view implementation for Minesweeper game.
    
    Invariants:
        - model must be a valid GameModel instance
        - controller must be a valid GameController instance
    """
    def __init__(self, model, controller):
        """
        Initializes the text-based view.
        
        Precondition:
            - model must be a valid GameModel instance
            - controller must be a valid GameController instance
        Postcondition:
            - View is initialized with valid model and controller references
        Invariant:
            - Model and controller references remain constant
        
        Maps to: __init__ in original minesweeper.py Minesweeper class
        """
        self.model = model
        self.controller = controller

    def display_board(self):
        """
        Displays the current state of the game board with mines and flag count.
        
        Precondition:
            - Model board must be initialized
            - Board size must be valid
        Postcondition:
            - Current board state is displayed in text format
        Invariant:
            - Display format remains consistent
        
        Maps to: setup() board display in original minesweeper.py
        """
        print("\nMinesweeper - Text View")
        print(f"Number of Mines: {self.model.mines_count}")
        print(f"Number of flags used: {self.model.flags_count}")
        
        print("    " + " ".join(f"{y:2}" for y in range(self.model.board_size[1])))
        
        for x, row in enumerate(self.model.board):
            row_display = [f"{x:2}  "]
            for cell in row:
                if not cell.is_revealed and not cell.is_flagged:
                    row_display.append(".")
                elif cell.is_flagged:
                    row_display.append("F")
                elif cell.is_mine:
                    row_display.append("*")
                elif cell.has_treasure:
                    row_display.append("T")
                elif cell.adjacent_mines > 0:
                    row_display.append(str(cell.adjacent_mines))
                else:
                    row_display.append(" ")
            print(" ".join(f"{item:2}" for item in row_display))
        print()

    def run(self):
        """
        Starts the text-based game loop.
        
        Precondition:
            - Model and controller must be initialized
        Postcondition:
            - Game loop runs until win/loss or quit
            - All user inputs are properly handled
        Invariant:
            - Game state remains consistent with user actions
        
        Maps to: mainloop() in original minesweeper.py
        """
        while True:
            self.display_board()
            print("\nEnter your move (row col action):")
            print("Actions: r(reveal), f(flag), q(quit)")
            move = input("Move: ").strip().lower().split()
            
            if len(move) == 1 and move[0] == 'q':
                print("Thank you for playing!")
                return
                
            if len(move) != 3:
                print("Invalid input. Please enter row, column, and action (reveal/flag).")
                continue
                
            try:
                x, y = int(move[0]), int(move[1])
                action = move[2]
                
                if not (0 <= x < self.model.board_size[0] and 
                    0 <= y < self.model.board_size[1]):
                    print(" ❌ Invalid coordinates. Please try again.")
                    continue
                    
                if action == "r":
                    result = self.controller.reveal_cell(x, y)
                    if result == "LOSS":
                        self.display_game_over(False)
                        return
                    elif result in ["WIN", "WIN_TREASURE"]:
                        self.display_game_over(True, result == "WIN_TREASURE")
                        return
                elif action == "f":
                    self.controller.toggle_flag(x, y)
                else:
                    print(" ❌ Invalid action. Use 'r' or 'f'.")
                    
            except ValueError:
                print(" ❌ Invalid input. Row and column must be integers.")
            except Exception as e:
                print(f" ❌ An unexpected error occurred: {e}")

    def update_flags_label(self):
        """
        Updates the displayed flag count.
        
        Precondition:
            - Model must have valid flags_count
        Postcondition:
            - Flag count display is updated
        Invariant:
            - Display matches model state
        
        Maps to: refreshLabels() flag display in original minesweeper.py
        """
        print(f"Number of flags Used: {self.model.flags_count}")

    def display_mines_count(self):
        """
        Displays the mines count.
        
        Precondition:
            - Model must have valid mines_count
        Postcondition:
            - Mines count is displayed
        Invariant:
            - Display matches model state
        
        Maps to: refreshLabels() mines display in original minesweeper.py
        """
        print(f"Number of Mines: {self.model.mines_count}")

    def update_cell(self, x, y):
        """
        Updates the view for a specific cell.
        
        Precondition:
            - x and y must be valid board coordinates
            - Cell at (x,y) must exist
        Postcondition:
            - Cell display is updated according to its state
        Invariant:
            - Display matches cell state in model
        
        Maps to: onClick() and onRightClick() cell updates in original minesweeper.py
        """
        cell = self.model.board[x][y]
        if cell.is_revealed:
            if cell.is_mine:
                print("*")
            elif cell.has_treasure:
                print("T")
            else:
                pass
        elif cell.is_flagged:
            print("F")
        else:
            print(".")

    def display_game_over(self, won, found_treasure=False):
        """
        Displays the game over message and final board.
        
        Precondition:
            - Game must be in end state (won or lost)
            - Board must be fully revealed
        Postcondition:
            - Final board state is displayed
            - Appropriate win/loss message shown
            - Player prompted for replay
        Invariant:
            - Game state remains unchanged during display
        
        Maps to: gameOver() in original minesweeper.py
        """
        print("\nGame Over!!")
        if won:
            if found_treasure:
                print("🎉 Congratulations! You have found the treasure! 💰")
            else:
                print("Congratulations! 🎉 You won the game! ")
        else:
            print("You hit a mine! 💥💣")

        print("\nRevealing final board:")
        
        print("    ", end="")
        for i in range(self.model.board_size[1]):
            print(f"{i:2}", end=" ")
        print()

        for x, row in enumerate(self.model.board):
            row_display = [f"{x:2}  "]
            for cell in row:
                if cell.is_mine and cell.is_flagged:
                    row_display.append("F ")
                elif cell.is_mine:
                    row_display.append("* ")
                elif not cell.is_mine and cell.is_flagged:
                    row_display.append("X ")
                elif cell.has_treasure:
                    row_display.append("T ")
                elif cell.adjacent_mines > 0:
                    row_display.append(f"{cell.adjacent_mines} ")
                else:
                    row_display.append("  ")
            print(" ".join(row_display))
        print()

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again == "yes":
            self.controller.restart_game()
            self.run()
        else:
            print("Thank you for playing!")
            exit(0)

    def reset_view(self):
        """
        Resets the text view for a new game.
        
        Precondition:
            - Controller must be ready for new game
        Postcondition:
            - View is reset to initial state
            - New game message displayed
        Invariant:
            - View state matches new game conditions
        
        Maps to: restart() view reset in original minesweeper.py
        """
        print("\nStarting a new game!")