import tkinter as tk

class InputLabel(tk.Label):
    def __init__(self, window):
        self.fontsize = 7
        self.string = tk.StringVar(value='')
        super().__init__(window, textvariable=self.string, relief='sunken', cursor='xterm', font=("Courier", self.fontsize+2), highlightthickness=1)
        
        self.bind('<Key>', func=self.process_key)
        self.grid(column=0, row=0)#, sticky='news')
        
        self.bind('<Button-1>', func=self.process_mouse)
        
        self.focus()
        
        
        self.pos = 0
        self.cursor = tk.Frame(self, height=16, width=1, background="black")
        self.visible = True
        self.cursor_visibility_loop()
        
    def cursor_visibility_loop(self):
        if self.visible:
            self.cursor.configure(background=self.master['background'])
            self.visible = False
        else:
            self.cursor.configure(background='black')
            self.visible = True
        self.master.after(500, self.cursor_visibility_loop)

    
    def update_cursor(self, newpos):
        self.pos = newpos
        self.pos = max(self.pos, 0)
        self.pos = min(self.pos, len(self.string.get()))
        self.cursor.place(x=self.pos*self.fontsize, y=1)
        
    def add_symbol(self, char):
        ss = self.string.get()
        left = ss[:self.pos]
        right = ss[self.pos:]
        self.string.set(left + char + right)
        self.update_cursor(self.pos+1)
        
    def remove_symbol(self):
        ss = self.string.get()
        left = ss[:self.pos][:-1]
        right = ss[self.pos:]
        self.string.set(left + right)
        self.update_cursor(self.pos-1)
    
    def process_key(self, event):
        if event.keysym == 'BackSpace':
            self.remove_symbol()
        elif event.keysym == 'Left':
            self.update_cursor(self.pos-1)
        elif event.keysym == 'Right':
            self.update_cursor(self.pos+1)
        elif event.keysym == 'Home':
            self.update_cursor(0)
        elif event.keysym == 'End':
            self.update_cursor(len(self.string.get()))
        elif event.char:
            if event.char.isprintable():
                self.add_symbol(event.char)
    
    def process_mouse(self, event):
        self.update_cursor(event.x // self.fontsize)
            
window = tk.Tk()
window.title("LabelEdit")

quit_btn = tk.Button(window, text='Quit', command=lambda: window.destroy())
quit_btn.grid(row=1, sticky='news')
inputlabel = InputLabel(window)

window.mainloop()
