import tkinter as tk
import re


class Figure:
    def __init__(self, fig=None, x1=None, y1=None, x2=None, y2=None, thick=None, color_fill=None, color_bord=None):
            
        self.type = fig
        self.coords = tuple(map(float, [x1, y1, x2, y2]))
        self.thickness = thick
        self.colors = (color_fill, color_bord)
    
    def draw(self, canvas):
        if self.type == "oval":
            canvas.create_oval(*self.coords, width=self.thickness, fill=self.colors[0], outline=self.colors[1])

    def __str__(self):
        return "%s <%.1f %.1f %.1f %.1f> %d %s %s\n" % (
            self.type,
            *map(float, self.coords),
            self.thickness,
            *self.colors
        )

class TextField(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        re_float = "\d*\.\d+|\d+"
        self.pattern = r"^([a-zA-Z]+) <(%s) (%s) (%s) (%s)> (\d+) (#[a-fA-F0-9]{6}) (#[a-fA-F0-9]{6})$" % (re_float, re_float, re_float, re_float)

        self.tag_configure('error', background='red')
        self.bind('<<Modified>>', self.draw_objects)

    def str2fig(self, my_str):
        fig, x1, y1, x2, y2, thick, color_fill, color_bord = re.split(self.pattern, my_str.strip())[1:-1]
        return Figure(fig, x1, y1, x2, y2, thick, color_fill, color_bord)

    def fig2str(self, figure):
        return str(figure)

    def draw_objects(self, data):
        self.tag_remove('error', 1.0, 'end')
        full_text = self.get("1.0", "end").split('\n')
        app.canvas.delete("all")
        for i, line in enumerate(full_text):
            try:
                fig = self.str2fig(line)
                fig.draw(app.canvas)
            except ValueError:
                self.tag_add('error', '%d.0' % (i+1), '%d.end' % (i+1))
        
        self.edit_modified(False)

# oval <10.0 10.0 210.0 210.0> 2 #aaaaaa #111111

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

        self.cur_color_fill = "#aaaaaa"
        self.cur_color_bg = "#111111"
        self.cur_thick = 2

    def create_widgets(self):
        self.txt_window = TextField()
        self.txt_window.grid(row=0, column=0, sticky='news')
        
        self.canvas = tk.Canvas()
        self.canvas.grid(row=0, column=1, sticky='news')
        # self.canvas.create_oval(100.0, 100.0, 200.0, 200.0)
    
    # def draw_all_objects(self):
    #     self.canvas.delete("all")
    #     print('here', len(self.all_objects))
    #     for fig in self.all_objects:
    #         fig.draw(self.canvas)

    # def create_figure(self, coords):
    #     fig = Figure(
    #         fig="oval", 
    #         x1 = coords[0], y1 = coords[1],
    #         x2 = coords[2], y2 = coords[3],
    #         thick = self.cur_thick,
    #         color_fill = self.cur_color_fill,
    #         color_bord = self.cur_color_bg
    #     )
    #     fig.draw(self.canvas)
    #     self.txt_window.insert(tk.END, str(fig))



    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)



app.mainloop()

