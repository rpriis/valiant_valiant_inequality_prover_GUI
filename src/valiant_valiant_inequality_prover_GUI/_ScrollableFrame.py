
import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, *args, start_height=65, start_width=None, x_scrollable=False, y_scrollable=False, **kwargs):
        super().__init__(*args, **kwargs)

        # canvas
        if start_width is None:
            self._scrolling_canvas = tk.Canvas(self, height=start_height)
        else:
            self._scrolling_canvas = tk.Canvas(self, height=start_height, width=start_width)

        # scrollbar
        if x_scrollable:
            x_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._scrolling_canvas.xview)
            x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self._scrolling_canvas.configure(xscrollcommand=x_scrollbar.set)

        if y_scrollable:
            y_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._scrolling_canvas.yview)
            y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._scrolling_canvas.configure(yscrollcommand=y_scrollbar.set)

        self._scrolling_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # final setup
        self._inner_frame = tk.Frame(self._scrolling_canvas)
        self._scrolling_canvas.create_window((0, 0), window=self._inner_frame, anchor="nw")

        self._inner_frame.bind(
            '<Configure>',
            lambda e: self._scrolling_canvas.configure(scrollregion=self._scrolling_canvas.bbox("all"))
        )

    def get_inner_frame(self):
        return self._inner_frame

    def change_height(self, new_height):
        self._scrolling_canvas.config(height=new_height)
        self._scrolling_canvas.pack()

