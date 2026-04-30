import tkinter as tk
from ui.game_controller import GameController

def run_ui():
    root = tk.Tk()
    controller = GameController(root)
    root.protocol("WM_DELETE_WINDOW", controller.close)
    root.mainloop()