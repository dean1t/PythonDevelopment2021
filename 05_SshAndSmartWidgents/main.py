import tkinter as tk
import re
# "oval <0.0 0.0 100.0 100.0> 2 #aaaaaa #111111"

class Figure:
    def __init__(self, my_str=None, fig=None, x1=None, y1=None, x2=None, y2=None, thick=None, color_fill=None, color_bord=None):
        if my_str is not None:
            re_float = "\d*\.\d+|\d+"
            pattern = r"^([a-zA-Z]+) <(%s) (%s) (%s) (%s)> (\d+) (#[a-fA-F0-9]{6}) (#[a-fA-F0-9]{6})$" % (re_float, re_float, re_float, re_float)
            fig, x1, y1, x2, y2, thick, color_fill, color_bord = re.split(pattern, my_str.strip())[1:-1]

        self.type = fig
        self.coords = tuple(map(float, [x1, y1, x2, y2]))
        self.thickness = thick
        self.colors = (color_fill, color_bord)
    
    def draw(self, canvas):
        if self.type == "oval":
            canvas.create_oval(*self.coords, width=self.thickness, fill=self.colors[0], outline=self.colors[1])

    def __str__(self):
        return "%s, <%.1f %.1f %.1f %.1f> %d %s %s\n" % (
            self.type,
            *map(float, self.coords),
            self.thickness,
            *self.colors
        )

    

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()
        self.create_widgets()
        

        self.cur_color_fill = "#aaaaaa"
        self.cur_color_bg = "#111111"
        self.cur_thick = 2

    def create_widgets(self):
        self.txt_window = tk.Text()
        self.txt_window.grid(row=0, column=0, sticky='news')
        # self.txt_window.pack(side='left')
        
        self.canvas = tk.Canvas()
        self.canvas.grid(row=0, column=1, sticky='news')
        # self.canvas.pack(side='right')
    
    def create_figure(self, coords):
        fig = Figure(
            fig="oval", 
            x1 = coords[0], y1 = coords[1],
            x2 = coords[2], y2 = coords[3],
            thick = self.cur_thick,
            color_fill = self.cur_color_fill,
            color_bord = self.cur_color_bg
        )
        fig.draw(self.canvas)
        self.txt_window.insert(tk.END, str(fig))



    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)


app.create_figure([10.0, 10.0, 210.0, 210.0])
app.create_figure([210.0, 210.0, 410.0, 410.0])
app.create_figure([410.0, 410.0, 610.0, 610.0])

app.mainloop()

