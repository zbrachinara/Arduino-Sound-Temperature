
from datastore import Data
from display import Display
from time import sleep
import tkinter as tk

root = tk.Tk()

data = Data()
display = Display(data, root)

if __name__ == '__main__':

    canvas = display.tk_obj
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def refresh():
        display.update() # gui loop (no event listeners)
        root.after(10, refresh)

    root.after(100, refresh)
    tk.mainloop()


