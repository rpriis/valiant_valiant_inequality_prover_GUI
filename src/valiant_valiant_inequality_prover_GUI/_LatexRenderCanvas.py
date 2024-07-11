
import constants as my_constants

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure


class LatexRenderCanvas(tk.Canvas):
    def __init__(self, parent, initial_text=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Render setup
        self._fig = matplotlib.figure.Figure(dpi=100, figsize=(1,1))
        self._ax = self._fig.add_axes([0, 0, 1, 1])
        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.X) # <><><><> fill=tk.X
        self._currently_on = False

        self._ax.get_xaxis().set_visible(False)
        self._ax.get_yaxis().set_visible(False)
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)
        self._ax.spines['bottom'].set_visible(False)
        self._ax.spines['left'].set_visible(False)

        if initial_text:
            self.replace_text(initial_text)

    def allow_interaction(self, ineq_num, hover_enter_func, hover_exit_func, clicked_func):
        self.bind('<Enter>', lambda event, f=hover_enter_func, i=ineq_num:  self.hover_enter(f, i))
        self.bind('<Leave>', lambda event, f=hover_exit_func: self.hover_exit(f))
        self._canvas.get_tk_widget().bind('<Button-1>', lambda event, f=clicked_func, i=ineq_num: self.clicked(f, i))

    def replace_text(self, new_text):
        self._ax.clear()
        rendered_text = self._ax.text(0, 0.5, new_text, fontsize=10)
        bounding_width = rendered_text.get_window_extent(renderer=self._canvas.get_renderer()).width
        self._canvas.get_tk_widget().configure(width=bounding_width, height=50)  # resize plot canvas

        self._canvas.draw()

    def set_funcs(self, on_hover, on_exit, on_click):
        pass

    def clicked(self, f, i):
        self._currently_on = not self._currently_on
        if self._currently_on:
            self._ax.set_facecolor(my_constants.SELECTED_COLOUR)
            self._canvas.draw()
        else:
            self._ax.set_facecolor(my_constants.HOVER_COLOUR)
            self._canvas.draw()
        f(i)
        self.event_generate('<Leave>')
        self.event_generate('<Enter>')

    def hover_enter(self, f, i):
        f(i)
        if not self._currently_on:
            self._ax.set_facecolor(my_constants.HOVER_COLOUR)
            self._canvas.draw()

    def hover_exit(self, f):
        f()
        if not self._currently_on:
            self._ax.set_facecolor('white')
            self._canvas.draw()


