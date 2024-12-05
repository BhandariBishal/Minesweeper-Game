class TextView:
    def __init__(self, model, controller):
        """
        Initializes the text-based view.
        """
        self.model = model
        self.controller = controller

    def display_board(self):
        """Displays the current state of the game board with mines and flag count."""
        print("\nMinesweeper - Text View")
        print(f"Mines: {self.model.mines_count}")
        print(f"Flags Used: {self.model.flags_count}")
        
        # Add extra space for column numbers and align them
        print("    " + " ".join(f"{y:2}" for y in range(self.model.board_size[1])))
        
        for x, row in enumerate(self.model.board):
            # Use fixed width for row numbers (2 characters + 2 spaces)
            row_display = [f"{x:2}  "]
            for cell in row:
                if not cell.is_revealed and not cell.is_flagged:
                    row_display.append(".")
                elif cell.is_flagged:
                    row_display.append("F")
                elif cell.is_mine:
                    row_display.append("*")
                elif cell.has_treasure:  # New: Show treasure as 'T'
                    row_display.append("T")
                elif cell.adjacent_mines > 0:
                    row_display.append(str(cell.adjacent_mines))
                else:
                    row_display.append(" ")
            # Join with double space to align with column numbers
            print(" ".join(f"{item:2}" for item in row_display))
        print()

    def run(self):
        """Starts the text-based game loop."""
        while True:
            self.display_board()
            print("\nEnter your move (row col action):")
            print("Actions: r(reveal), f(flag), q(quit)")
            move = input("Move: ").strip().lower().split()
            
            if len(move) == 1 and move[0] == 'q':
                print("Thanks for playing!")
                return
                
            if len(move) != 3:
                print("Invalid input. Please enter row, column, and action (reveal/flag).")
                continue
                
            try:
                x, y = int(move[0]), int(move[1])
                action = move[2]
                
                if not (0 <= x < self.model.board_size[0] and 
                    0 <= y < self.model.board_size[1]):
                    print("Invalid coordinates. Please try again.")
                    continue
                    
                if action == "r":
                    result = self.controller.reveal_cell(x, y)
                    if result == "LOSS":
                        self.display_game_over(False)
                        return
                    elif result in ["WIN", "WIN_TREASURE"]:  # New: Handle treasure win
                        self.display_game_over(True, result == "WIN_TREASURE")
                        return
                elif action == "f":
                    self.controller.toggle_flag(x, y)
                else:
                    print("Invalid action. Use 'r' or 'f'.")
                    
            except ValueError:
                print("Invalid input. Row and column must be integers.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def update_flags_label(self):
        """Updates the displayed flag count."""
        print(f"Flags Used: {self.model.flags_count}")

    def display_mines_count(self):
        """Displays the mines count."""
        print(f"Mines: {self.model.mines_count}")

    def update_cell(self, x, y):
        """Updates the view for a specific cell."""
        cell = self.model.board[x][y]
        if cell.is_revealed:
            if cell.is_mine:
                print("*")
            elif cell.has_treasure:  # New: Show treasure
                print("T")
            elif cell.adjacent_mines > 0:
                print(cell.adjacent_mines)
            else:
                print(" ")
        elif cell.is_flagged:
            print("F")
        else:
            print(".")

    def display_game_over(self, won, found_treasure=False):
        """Displays the game over message and final board."""
        print("\nGame Over!")
        if won:
            if found_treasure:
                print("🎉 Congratulations! You found the treasure! 🎉")
            else:
                print("🎉 Congratulations! You won the game! 🎉")
        else:
            print("💥 You hit a mine! 💥")

        print("\nRevealing final board:")
        
        # Print column numbers with proper alignment
        print("    ", end="")  # 4 spaces for row number column
        for i in range(self.model.board_size[1]):
            print(f"{i:2}", end=" ")  # 2 spaces for each column number
        print()

        # Print board with aligned content
        for x, row in enumerate(self.model.board):
            row_display = [f"{x:2}  "]  # 2 spaces for row number + 2 spaces padding
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
                    row_display.append("  ")  # Two spaces for empty cells
            print(" ".join(row_display))
        print()

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again == "yes":
            self.controller.restart_game()
            self.run()
        else:
            print("Thanks for playing!")
            exit(0)

    def reset_view(self):
        """Resets the text view for a new game."""
        print("\nStarting a new game!")