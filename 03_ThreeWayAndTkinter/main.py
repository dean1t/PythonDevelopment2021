import tkinter as tk
from tkinter import *
import random

window = Tk()
window.title("15")
window.geometry('400x400')

btn_size = 2
clear_spot = {'column':3, 'row':3}

def count_inverse(order):
    count = 0
    for i in range(0, len(order)):
        for j in range(i, len(order)):
            if order[i] > order[j]:
                count += 1
    return count

def make_solvable(order):
    if count_inverse(order) % 2 == 0:
        return order
    else:
        _max = max(order)
        new_order = order[:]
        new_order[order.index(_max)] = _max-1
        new_order[order.index(_max-1)] = _max
        return new_order

def new_game():
    global clear_spot
    new_order = list(range(15))
    random.shuffle(new_order)
    new_order = make_solvable(new_order)
    for i, btn_idx in enumerate(new_order):
        btns[btn_idx].grid(column=i%4*btn_size, row=i//4*btn_size+1, columnspan=btn_size, rowspan=btn_size, sticky=tk.N+tk.E+tk.S+tk.W)
    clear_spot = {'column':3, 'row':3}

def exit_game():
    window.destroy()

def make_move_fn(btn_idx):
    idx = btn_idx
    def move_btn():
        global clear_spot
        grid_info = btns[idx].grid_info()
        col = grid_info['column'] // grid_info['columnspan']
        row = grid_info['row'] // grid_info['rowspan']
        if abs(clear_spot['column'] - col) + abs(clear_spot['row'] - row) > 1:
            return
        btns[idx].grid_configure(column=clear_spot['column']*btn_size, row=clear_spot['row']*btn_size+1)
        clear_spot = {'column': col, 'row': row}
    return move_btn

for i in range(4*btn_size):
    window.grid_columnconfigure(i, weight=10, pad=1)
    window.grid_rowconfigure(i+1, weight=10, pad=1)

btns = [Button(window, text=str(i+1), command=make_move_fn(i)) for i in range(15)]

new_btn = Button(window, text='New', command=new_game)
new_btn.grid(column=1, row=0, columnspan=btn_size, sticky=tk.N+tk.E+tk.S+tk.W)

exit_btn = Button(window, text='Exit', command=exit_game)
exit_btn.grid(column=5, row=0, columnspan=btn_size, sticky=tk.N+tk.E+tk.S+tk.W)

new_game()
    # print(btn.grid_info())
# print(window.grid_bbox())

window.mainloop()