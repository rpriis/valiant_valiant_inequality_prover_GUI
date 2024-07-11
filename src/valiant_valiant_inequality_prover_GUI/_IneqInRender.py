
from _LatexRenderCanvas import LatexRenderCanvas

import tkinter as tk


class IneqInRender(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # canvas
        self._scrolling_canvas = tk.Canvas(self, height=50)
        self._scrolling_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # scrollbar
        x_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._scrolling_canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self._scrolling_canvas.configure(xscrollcommand=x_scrollbar.set)

        # final setup
        self._inner_frame = tk.Frame(self._scrolling_canvas)
        self._scrolling_canvas.create_window((0, 0), window=self._inner_frame, anchor="nw")
        self._inner_canvas = LatexRenderCanvas(self._inner_frame)
        self._inner_canvas.pack(side=tk.TOP, expand=True, fill=tk.X)

        # make scrolling canvas resize whenever _inner_canvas changes size (window changes size)
        self._inner_canvas.bind(
            '<Configure>', lambda e: self._scrolling_canvas.configure(scrollregion=self._scrolling_canvas.bbox("all"))
        )

    def replace_text(self, new_text):
        self._inner_canvas.replace_text(new_text)