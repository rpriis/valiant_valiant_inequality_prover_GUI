
from _LatexRenderCanvas import LatexRenderCanvas
import valiant_valiant_inequality_prover.prover as vvip

import tkinter as tk


class DecompIneqFrame(tk.Frame):
    def __init__(self, parent, suffix_text, hover_enter_func, hover_exit_func, clicked_func, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._header_text = tk.Label(self, text='', anchor=tk.W)
        self._header_text.pack(side=tk.TOP, expand=True, fill=tk.X)
        self._suffix_text = suffix_text

        self._render_ineqs = []

        self._hover_enter_func = hover_enter_func
        self._hover_exit_func = hover_exit_func
        self._clicked_func = clicked_func

    def set(self, m, powers, simplify):
        for r in self._render_ineqs:
            r.destroy()
        self._render_ineqs = []  # note: does, in fact, release memory (as of current python version)

        num_ineqs = len(powers)
        if num_ineqs > 0:
            suf = self._suffix_text + ' inequalities:' if num_ineqs > 1 else self._suffix_text + ' inequality:'
            self._header_text.configure(text='%d ' % num_ineqs + suf)

            x = [vvip.get_latex(m[i], mode='raw', include_geq=False, simplify=simplify) for i in
                 range(num_ineqs)]
            for i in range(num_ineqs):
                s = '$' + r'\left[' + x[i] + r'\right]^{' + '%3.3g' % powers[i] + r'}\geq1$'
                k = LatexRenderCanvas(self, s)
                k.pack(side=tk.TOP, expand=True, fill=tk.X)
                if m.shape[2] == 3: # 2D; will render
                    k.allow_interaction(i, self._hover_enter_func, self._hover_exit_func, self._clicked_func)
                self._render_ineqs.append(k)
        else:
            self._header_text.configure(text='')

    def clear(self):
        for r in self._render_ineqs:
            r.destroy()
        self._render_ineqs = []  # does, in fact, release memory as of current python version
        self._header_text.configure(text='')

