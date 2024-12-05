from tkinter import *
from tkinter import messagebox

class GUIView:
    """
    Graphical user interface for the Minesweeper game using Tkinter.
    Handles all visual elements and user interactions.
    """
    def __init__(self, tk, model, controller):
        """
        Initializes the GUI view.
        """
        self.tk = tk
        self.model = model
        if self.model.board_size == (0, 0):
            raise ValueError("GameModel board_size is not initialized. Did you call initialize_board?")

        self.controller = controller

        self.frame = Frame(self.tk)
        self.frame.pack()
        self.timer_running = False
        self.start_timer()

        # Load images
        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "treasure": PhotoImage(file="images/tile_treasure.gif"),  # New: treasure image
            "numbers": [PhotoImage(file=f"images/tile_{i}.gif") for i in range(1, 9)]
        }

        self.labels = {
            "time": Label(self.frame, text="00:00:00"),
            "mines": Label(self.frame, text=f"Mines: {self.model.mines_count}"),
            "flags": Label(self.frame, text=f"Flags: {self.model.flags_count}")
        }
        self.labels["time"].grid(row=0, column=0, columnspan=max(1, self.model.board_size[1]))
        self.labels["mines"].grid(row=self.model.board_size[0] + 1, column=0, columnspan=4)
        self.labels["flags"].grid(row=self.model.board_size[0] + 1, column=4, columnspan=4)

        self.setup_board()

    def setup_board(self):
        """Sets up the GUI board based on the model."""
        for x, row in enumerate(self.model.board):
            for y, cell in enumerate(row):
                button = Button(self.frame, image=self.images["plain"])
                # Left click for reveal
                button.bind("<Button-1>", lambda event, x=x, y=y: self.controller.reveal_cell(x, y))
                # Right click for flag - multiple bindings for cross-platform support
                button.bind("<Button-2>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))  # For Mac
                button.bind("<Button-3>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))  # For Windows
                button.bind("<Control-Button-1>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))  # Alternative for Mac
                button.grid(row=x + 1, column=y)
                cell.button = button
        # Update mines label
        self.labels["mines"].config(text=f"Mines: {self.model.mines_count}")

    def update_cell(self, x, y):
        """
        Updates the GUI for a single cell.
        """
        cell = self.model.board[x][y]
        if cell.is_revealed:
            if cell.is_mine:
                cell.button.config(image=self.images["mine"])
            elif cell.has_treasure:  # New: Show treasure if revealed
                cell.button.config(image=self.images["treasure"])
            elif cell.adjacent_mines > 0:
                cell.button.config(image=self.images["numbers"][cell.adjacent_mines - 1])
            else:
                cell.button.config(image=self.images["clicked"])
        elif cell.is_flagged:
            cell.button.config(image=self.images["flag"])
        else:
            cell.button.config(image=self.images["plain"])

    def display_game_over(self, won):
        """
        Displays the game over message and reveals all mines.
        """
        self.stop_timer()

        # Reveal all mines and wrongly flagged cells
        for row in self.model.board:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    cell.button.config(image=self.images["mine"])
                elif not cell.is_mine and cell.is_flagged:
                    cell.button.config(image=self.images["wrong"])
                elif cell.has_treasure:  # Show treasures at game over
                    cell.button.config(image=self.images["treasure"])

        # Show game over message with treasure win condition
        message = "You found a treasure! You Win!" if won == "WIN_TREASURE" else "You Win!" if won else "You Lose!"

        if messagebox.askyesno("Game Over", f"{message} Play again?"):
            # Clean up old buttons before destroying frame
            for row in self.model.board:
                for cell in row:
                    if hasattr(cell, 'button'):
                        cell.button.destroy()
                        
            # Clean up old frame
            self.frame.destroy()
            
            # Create new frame
            self.frame = Frame(self.tk)
            self.frame.pack()
            
            # Reset timer label and game status labels
            self.labels = {
                "time": Label(self.frame, text="00:00:00"),
                "mines": Label(self.frame, text=f"Mines: {self.model.mines_count}"),
                "flags": Label(self.frame, text=f"Flags: {self.model.flags_count}")
            }
            self.labels["time"].grid(row=0, column=0, columnspan=max(1, self.model.board_size[1]))
            self.labels["mines"].grid(row=self.model.board_size[0] + 1, column=0, columnspan=4)
            self.labels["flags"].grid(row=self.model.board_size[0] + 1, column=4, columnspan=4)
            
            # Restart game and setup new board
            self.controller.restart_game()
            self.setup_board()  # Add this line to create new buttons
            self.start_timer()
        else:
            self.tk.quit()

    def update_flags_label(self):
        """
        Updates the flag count label in the GUI.
        """
        self.labels["flags"].config(text=f"Flags: {self.model.flags_count}")

    def start_timer(self):
        """
        Starts the game timer.
        """
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """
        Stops the game timer.
        """
        self.timer_running = False

    def update_timer(self):
        """
        Updates the timer label in the GUI.
        """
        if self.model.start_time and self.timer_running:
            from datetime import datetime
            elapsed_time = datetime.now() - self.model.start_time
            time_str = str(elapsed_time).split('.')[0]  # Format as H:M:S
            self.labels["time"].config(text=time_str)

        # Call this method again after 1 second
        if self.timer_running:
            self.tk.after(1000, self.update_timer)