import tkinter as tk
from controller import *

if __name__ == '__main__': #inicia o código
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()