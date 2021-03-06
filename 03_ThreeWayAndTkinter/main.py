import tkinter as tk
from tkinter import *

window = Tk()
window.title("15")
window.geometry('400x400')

btn_size = 1
clear_spot = {'column':3, 'row':4}

def make_move_fn(btn_idx):
    idx = btn_idx
    def move_btn():
        global clear_spot
        grid_info = btns[idx].grid_info()
        col = grid_info['column'] // grid_info['columnspan']
        row = grid_info['row'] // grid_info['rowspan']
        if abs(clear_spot['column'] - col) + abs(clear_spot['row'] - row) > 1:
            return
        btns[idx].grid_configure(column=clear_spot['column']*btn_size, row=clear_spot['row']*btn_size)
        clear_spot = {'column': col, 'row': row}
    return move_btn

for i in range(4):
    window.grid_columnconfigure(i, weight=10, pad=1)
    window.grid_rowconfigure(i+1, weight=10, pad=1)

btns = [Button(window, text=str(i+1), command=make_move_fn(i)) for i in range(15)]
for i, btn in enumerate(btns):
    btn.grid(column=i%4*btn_size, row=i//4*btn_size+1, columnspan=btn_size, rowspan=btn_size, sticky=tk.N+tk.E+tk.S+tk.W)
    # print(btn.grid_info())
# print(window.grid_bbox())

window.mainloop()