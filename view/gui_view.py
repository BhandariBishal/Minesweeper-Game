from tkinter import *
from tkinter import messagebox

class GUIView:
    """
    Graphical user interface for the Minesweeper game using Tkinter.
    Handles all visual elements and user interactions.
    
    Invariants:
        - model must be a valid GameModel instance
        - controller must be a valid GameController instance
        - tk must be a valid Tkinter root instance
        - All image files must exist in the specified paths
    """
    def __init__(self, tk, model, controller):
        """
        Initializes the GUI view.
        
        Precondition:
            - tk must be a valid Tkinter root instance
            - model must be initialized with valid board size
            - controller must be a valid GameController instance
            - All required image files must exist in images/ directory
        Postcondition:
            - GUI elements are initialized and displayed
            - Timer is started
            - Board is set up with proper buttons and bindings
        Invariant:
            - Frame and labels remain properly positioned
        
        Maps to: __init__ in original minesweeper.py Minesweeper class
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

        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "treasure": PhotoImage(file="images/tile_treasure.gif"),
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
        """
        Sets up the GUI board based on the model.
        
        Precondition:
            - Model board must be initialized
            - Frame must exist
            - All images must be loaded
        Postcondition:
            - All cells have corresponding buttons
            - All buttons have proper event bindings
            - Mines label is updated
        Invariant:
            - Button grid matches model board dimensions
        
        Maps to: setup() in original minesweeper.py
        """
        for x, row in enumerate(self.model.board):
            for y, cell in enumerate(row):
                button = Button(self.frame, image=self.images["plain"])
                button.bind("<Button-1>", lambda event, x=x, y=y: self.controller.reveal_cell(x, y))
                button.bind("<Button-2>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))
                button.bind("<Button-3>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))
                button.bind("<Control-Button-1>", lambda event, x=x, y=y: self.controller.toggle_flag(x, y))
                button.grid(row=x + 1, column=y)
                cell.button = button
        self.labels["mines"].config(text=f"Mines: {self.model.mines_count}")

    def update_cell(self, x, y):
        """
        Updates the GUI for a single cell.
        
        Precondition:
            - x and y must be valid board coordinates
            - Cell at (x,y) must exist
            - All images must be loaded
        Postcondition:
            - Cell button displays correct image based on state
        Invariant:
            - Button state matches cell state in model
        
        Maps to: onClick() and onRightClick() cell updates in original minesweeper.py
        """
        cell = self.model.board[x][y]
        if cell.is_revealed:
            if cell.is_mine:
                cell.button.config(image=self.images["mine"])
            elif cell.has_treasure:
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
        
        Precondition:
            - Game must be in end state (won or lost)
            - All cells must have valid buttons
        Postcondition:
            - All mines and wrong flags are revealed
            - Game over dialog is shown
            - Game either restarts or closes based on user choice
        Invariant:
            - All cells remain accessible during cleanup
        
        Maps to: gameOver() in original minesweeper.py
        """
        self.stop_timer()

        for row in self.model.board:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    cell.button.config(image=self.images["mine"])
                elif not cell.is_mine and cell.is_flagged:
                    cell.button.config(image=self.images["wrong"])
                elif cell.has_treasure:
                    cell.button.config(image=self.images["treasure"])

        message = "You found a treasure! 💰 You have won the Game!" if won == "WIN_TREASURE" else "You Win!" if won else "You Lose! 💣"

        if messagebox.askyesno("Game Over", f"{message} Play again?"):
            for row in self.model.board:
                for cell in row:
                    if hasattr(cell, 'button'):
                        cell.button.destroy()
            
            self.frame.destroy()
            self.frame = Frame(self.tk)
            self.frame.pack()
            
            self.labels = {
                "time": Label(self.frame, text="00:00:00"),
                "mines": Label(self.frame, text=f"Mines: {self.model.mines_count}"),
                "flags": Label(self.frame, text=f"Flags: {self.model.flags_count}")
            }
            self.labels["time"].grid(row=0, column=0, columnspan=max(1, self.model.board_size[1]))
            self.labels["mines"].grid(row=self.model.board_size[0] + 1, column=0, columnspan=4)
            self.labels["flags"].grid(row=self.model.board_size[0] + 1, column=4, columnspan=4)
            
            self.controller.restart_game()
            self.setup_board()
            self.start_timer()
        else:
            self.tk.quit()

    def update_flags_label(self):
        """
        Updates the flag count label in the GUI.
        
        Precondition:
            - Model must have valid flags_count
            - Flags label must exist
        Postcondition:
            - Flags label shows current flag count
        Invariant:
            - Display matches model state
        
        Maps to: refreshLabels() flag display in original minesweeper.py
        """
        self.labels["flags"].config(text=f"Flags: {self.model.flags_count}")

    def start_timer(self):
        """
        Starts the game timer.
        
        Precondition:
            - Timer label must exist
            - Timer must not be already running
        Postcondition:
            - Timer is running
            - Timer display begins updating
        Invariant:
            - Only one timer can run at a time
        
        Maps to: updateTimer() initialization in original minesweeper.py
        """
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """
        Stops the game timer.
        
        Precondition:
            - Timer must be running
        Postcondition:
            - Timer is stopped
            - Timer display stops updating
        Invariant:
            - Timer state remains consistent
        
        Maps to: gameOver() timer handling in original minesweeper.py
        """
        self.timer_running = False

    def update_timer(self):
        """
        Updates the timer label in the GUI.
        
        Precondition:
            - Timer label must exist
            - Timer must be running
            - Model start_time must be valid if game started
        Postcondition:
            - Timer display is updated
            - Next update is scheduled if timer is running
        Invariant:
            - Time display format remains consistent
        
        Maps to: updateTimer() in original minesweeper.py
        """
        if self.model.start_time and self.timer_running:
            from datetime import datetime
            elapsed_time = datetime.now() - self.model.start_time
            time_str = str(elapsed_time).split('.')[0]
            self.labels["time"].config(text=time_str)

        if self.timer_running:
            self.tk.after(1000, self.update_timer)