from tkinter import *
from tkinter import ttk
import program_ui

root = Tk()
root.title("CRITICAL PATH")
root.geometry("250x200")

root.grid_rowconfigure(index=0, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)

open_button_bd_1 = ttk.Button(text="Ввод данных", command=program_ui.input_data)
open_button_bd_1.grid(column=0, row=0, sticky=NSEW, padx=10)

open_button_bd_2 = ttk.Button(text="Оптимизация", command=program_ui.optimisation)
open_button_bd_2.grid(column=1, row=0, sticky=NSEW, padx=10)

root.mainloop()
