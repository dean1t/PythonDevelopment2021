import tkinter as tk
import re

FLOAT_PATTERN = r"\d*\.\d+|\d+"
FIGURE_PATTERN = r"^<(%s) (%s) (%s) (%s)> (\d+) (#[a-fA-F0-9]{6}) (#[a-fA-F0-9]{6})$" % (FLOAT_PATTERN, FLOAT_PATTERN, FLOAT_PATTERN, FLOAT_PATTERN)

class Figure:
    def __init__(self, my_str):
        *self.coords, self.thick, self.color_fill, self.color_bord = re.split(FIGURE_PATTERN, my_str.strip())[1:-1]
        self.coords = tuple(map(float, self.coords))
    
    def draw(self, canvas):
        canvas.create_oval(*self.coords, width=self.thick, fill=self.color_fill, outline=self.color_bord)

    def __str__(self):
        return "<%.1f %.1f %.1f %.1f> %d %s %s\n" % (
            self.type,
            *map(float, self.coords),
            self.thick,
            self.color_fill, self.color_bord
        )

class TextField(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tag_configure('error', background='red')
        self.bind('<<Modified>>', self.update_text_field)

    def update_text_field(self, args):
        self.tag_remove('error', '1.0', 'end')

        full_text = self.get("1.0", "end").split('\n')
        written_figures = []
        for i, line in enumerate(full_text):
            try:
                fig = Figure(line)
                written_figures.append(fig)
                # fig.draw(app.canvas)
            except:
                self.tag_add('error', '%d.0' % (i+1), '%d.end' % (i+1))
        
        self.master.draw_figures(written_figures)
        self.edit_modified(False)

# <10.0 10.0 210.0 210.0> 2 #aaaaaa #111111

class CanvasField(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.text = TextField(self)
        self.text.grid(row=0, column=0, sticky="news")

        self.canvas = CanvasField(self)
        self.canvas.grid(row=0, column=1, sticky="news")

    def draw_figures(self, figures):
        self.canvas.delete("all")
        for fig in figures:
            fig.draw(self.canvas)


app = Application()
app.mainloop()
