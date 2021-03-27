import tkinter as tk
import re
import random

FLOAT_PATTERN = r"[+-]?\d*\.\d+|\d+"
FIGURE_PATTERN = r"^<(%s) (%s) (%s) (%s)> (\d+) (#[a-fA-F0-9]{6}) (#[a-fA-F0-9]{6})$" % (FLOAT_PATTERN, FLOAT_PATTERN, FLOAT_PATTERN, FLOAT_PATTERN)

class Figure:
    def __init__(self, my_str):
        if my_str is None:
            # random creating
            self.coords = None # suppose self.coord will fill up soon
            self.thick = random.randint(1, 4)
            self.color_fill = '#%06x' % random.randint(0, 256*256*256-1)
            self.color_bord = '#%06x' % random.randint(0, 256*256*256-1)
        else:
            *self.coords, self.thick, self.color_fill, self.color_bord = re.split(FIGURE_PATTERN, my_str.strip())[1:-1]
            self.coords = tuple(map(float, self.coords))
    
    def draw(self, canvas, tag):
        canvas.create_oval(*self.coords, width=self.thick, fill=self.color_fill, outline=self.color_bord, tags=tag)

    def __str__(self):
        return "<%.1f %.1f %.1f %.1f> %s %s %s" % (
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
                written_figures.append((fig, i+1))
            except:
                self.tag_add('error', '%d.0' % (i+1), '%d.end' % (i+1))
        
        self.master.draw_figures(written_figures)
        self.edit_modified(False)
    
    def commit_move(self, line, dx, dy):
        newfig = Figure(self.get(line+'.0', line+'.end'))
        newfig.coords = (
            newfig.coords[0] + dx, newfig.coords[1] + dy,
            newfig.coords[2] + dx, newfig.coords[3] + dy,
        )
        self.delete(line+'.0', line+'.end')
        self.insert(line+'.0', str(newfig))

    def commit_creating(self, figure):
        cur_data = self.get('1.0', 'end')
        if len(cur_data) > 1 and cur_data[-2] != '\n':
            start = '\n'
        else:
            start = ''
        self.insert('end', start + str(figure) + '\n')

# <10.0 10.0 210.0 210.0> 2 #aaaaaa #111111
# <210.0 10.0 310.0 210.0> 2 #aaaaaa #111111
# <10.0 110.0 110.0 310.0> 2 #aaaaaa #111111


class CanvasField(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind('<Button-1>', self.click)
        self.bind('<ButtonRelease-1>', self.release)

        self.moving_dict = {
            'is_moving': False,
        }
        self.creating_dict = {
            'is_creating': False
        }
        # self.bind('<Motion>', self.move)
    
    def click(self, event):
        cur_figures = self.find_overlapping(event.x, event.y, event.x, event.y)
        if len(cur_figures) > 0:
            self.moving_dict = {
                'is_moving': True,
                'old_figure_idx': cur_figures[-1],
                'old_center': (event.x, event.y)
            }
        else:
            fig = Figure(None)
            self.creating_dict = {
                'is_creating': True,
                'top_left': (event.x, event.y),
                'figure': fig
            }

    def release(self, event):
        if self.moving_dict['is_moving']:
            dx = event.x - self.moving_dict['old_center'][0]
            dy = event.y - self.moving_dict['old_center'][1]
            self.master.text.commit_move(self.gettags(self.moving_dict['old_figure_idx'])[0], dx, dy)
            self.moving_dict['is_moving'] = False

        elif self.creating_dict['is_creating']:
            fig = self.creating_dict['figure']
            fig.coords = (
                *self.creating_dict['top_left'],
                event.x, event.y
            )
            if abs(fig.coords[0] - fig.coords[2]) + abs(fig.coords[1] - fig.coords[3]) > 5:
                self.master.text.commit_creating(fig)
            self.creating_dict['is_creating'] = False


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
        for fig, line in figures:
            fig.draw(self.canvas, tag=str(line))


app = Application()
app.mainloop()
