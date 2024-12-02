
import platform

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.bind_events()
        self.model.add_observer(self.view)

    def bind_events(self):
        for (row, column), button in self.view.buttons.items():
            button.bind('<Button-1>', self.on_left_click_wrapper(row, column))
            button.bind('<Button-2>' if platform.system() == 'Darwin' else '<Button-3>', self.on_right_click_wrapper(row, column))

    def on_left_click_wrapper(self, row, column):
        return lambda event: self.on_left_click(row, column)

    def on_right_click_wrapper(self, row, column):
        return lambda event: self.on_right_click(row, column)

    def on_left_click(self, row, column):
        self.model.reveal_cell(row, column)
        # ...additional logic...

    def on_right_click(self, row, column):
        self.model.flag_cell(row, column)
        # ...additional logic...