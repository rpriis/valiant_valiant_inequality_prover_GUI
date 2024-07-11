
from helper_funcs import *

import valiant_valiant_inequality_prover.prover as vvip

import tkinter as tk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
import numpy as np
import math


class GraphOut(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fig = matplotlib.figure.Figure(figsize=(10, 10), dpi=100)
        self._ax = fig.gca()
        self._ax.autoscale(False)

        self._canvas = FigureCanvasTkAgg(fig, master=self)
        self._canvas.draw()
        toolbar = NavigationToolbar2Tk(self._canvas, self)
        self._canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)

        self._initial_points = None
        self._holder_moves = None
        self._lp_mon_moves = None
        self._rendered_points = None

        self._is_2d_render = True

        self._holder_moves_status = None
        self._lp_mon_moves_status = None

        self._preview_objects = []
        self._point_objects = []

        self._initial_xlim = None
        self._initial_ylim = None

    def _update_points_render(self, m, refresh_view=True):
        initial_x_lims = self._ax.get_xlim()
        initial_y_lims = self._ax.get_ylim()
        self._ax.clear()

        if refresh_view:
            self._ax.set_xlim(initial_x_lims)
            self._ax.set_ylim(initial_y_lims)

        if m is None:
            return
        for i in range(m.shape[0]):
            self._ax.plot(m[i, 0], m[i, 1], 'ko')

    def set_initial_points(self, m):
        self._is_2d_render = m.shape[1]-1 == 2
        if not self._is_2d_render:
            self._ax.clear()
            self._canvas.draw()
            return
        self._initial_points = m
        self._update_points_render(self._initial_points, refresh_view=False)
        self._holder_moves = None
        self._lp_mon_moves = None
        self._holder_moves_status = None
        self._lp_mon_moves_status = None
        self._initial_xlim, self._initial_ylim = self._ax.get_xlim(), self._ax.get_ylim()
        self._canvas.draw()

    def _update_moved_state(self):
        n = len(self._initial_points)
        # number of 'active' moves
        num_holder = self._holder_moves_status.sum()
        num_lp_mon = self._lp_mon_moves_status.sum()
        holders = self._holder_moves_status.nonzero()[0]
        lp_mons = self._lp_mon_moves_status.nonzero()[0]

        self._rendered_points = np.zeros((n + 3*num_holder + 2*num_lp_mon, self._initial_points.shape[1]))
        self._rendered_points[:n] = self._initial_points.copy()

        for i in range(num_holder):
            self._rendered_points[n+3*i:n+3*i+3] = self._holder_moves[holders[i]]
        for i in range(num_lp_mon):
            self._rendered_points[n+3*num_holder+2*i:n+3*num_holder+2*i+2] = self._lp_mon_moves[lp_mons[i]]

        output_points = vvip.merge_common_matrix_expressions(self._rendered_points)
        self._update_points_render(output_points)

    def set_possible_moves(self, holder_moves, holder_powers, lp_mon_moves, lp_mon_powers):
        self._holder_moves = apply_negative_matrix_powers(holder_moves, holder_powers)
        self._lp_mon_moves = apply_negative_matrix_powers(lp_mon_moves, lp_mon_powers)
        self._holder_moves_status = np.full(len(holder_powers), False)
        self._lp_mon_moves_status = np.full(len(lp_mon_powers), False)

    def cancel_preview(self):
        for o in self._preview_objects:
            o.remove()
        self._preview_objects = []
        self._canvas.draw()

    def change_title_text(self, text):
        self.config(text=text)

    def _draw_arrow(self, p1, p2):
        arrow_length = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        arrow_props = dict(color='black', width=0.4, headwidth=8, headlength=10, shrink=0.076/arrow_length)
        arrow = self._ax.annotate("", xy=p1, xytext=p2, arrowprops=arrow_props, annotation_clip=False)  # no clip_rect
        arrow.arrow_patch.set_clip_box(self._ax.bbox)
        return arrow

    def preview_holder(self, i):
        if not self._is_2d_render:
            return
        self.cancel_preview()
        if self._holder_moves_status[i]:  # outward
            self._preview_objects.append(self._draw_arrow(self._holder_moves[i, 0, 0:2], self._holder_moves[i, 2, 0:2]))
            self._preview_objects.append(self._draw_arrow(self._holder_moves[i, 1, 0:2], self._holder_moves[i, 2, 0:2]))
        else:  # inward
            self._preview_objects.append(self._draw_arrow(self._holder_moves[i, 2, 0:2], self._holder_moves[i, 0, 0:2]))
            self._preview_objects.append(self._draw_arrow(self._holder_moves[i, 2, 0:2], self._holder_moves[i, 1, 0:2]))

        self._preview_objects.append(self._ax.plot(self._holder_moves[i, 0, 0], self._holder_moves[i, 0, 1], 'c.')[0])
        self._preview_objects.append(self._ax.plot(self._holder_moves[i, 1, 0], self._holder_moves[i, 1, 1], 'c.')[0])
        self._preview_objects.append(self._ax.plot(self._holder_moves[i, 2, 0], self._holder_moves[i, 2, 1], 'c.')[0])
        self._canvas.draw()

    def preview_lp_mon(self, i):
        if not self._is_2d_render:
            return
        self.cancel_preview()
        if self._lp_mon_moves_status[i]:
            self._preview_objects.append(self._draw_arrow(self._lp_mon_moves[i, 0, 0:2], self._lp_mon_moves[i, 1, 0:2]))
        else:
            self._preview_objects.append(self._draw_arrow(self._lp_mon_moves[i, 1, 0:2], self._lp_mon_moves[i, 0, 0:2]))

        self._preview_objects.append(self._ax.plot(self._lp_mon_moves[i, 0, 0], self._lp_mon_moves[i, 0, 1], 'c.')[0])
        self._preview_objects.append(self._ax.plot(self._lp_mon_moves[i, 1, 0], self._lp_mon_moves[i, 1, 1], 'c.')[0])
        self._canvas.draw()

    def holder_ineq_clicked(self, i):
        if not self._is_2d_render:
            return
        self._holder_moves_status[i] = not self._holder_moves_status[i]
        self._update_moved_state()

    def lp_mon_ineq_clicked(self, i):
        if not self._is_2d_render:
            return
        self._lp_mon_moves_status[i] = not self._lp_mon_moves_status[i]
        self._update_moved_state()