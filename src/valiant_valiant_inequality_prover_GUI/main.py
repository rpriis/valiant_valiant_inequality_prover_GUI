
from helper_funcs import *
import constants as my_constants

from _GraphOut import GraphOut
from _IneqGrid import IneqGrid
from _DimChanger import DimChanger
from _IneqInRender import IneqInRender
from _UserMessage import UserMessage
from _DecompIneqFrame import DecompIneqFrame
from _ScrollableFrame import ScrollableFrame


import tkinter as tk
import numpy as np
import pyperclip
import matplotlib
import valiant_valiant_inequality_prover.prover as vvip

matplotlib.use('TkAgg')


class _GUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.option_add("*Background", "white")

        self._allow_graphic_interaction = True
        starting_matrix = matlab_matrix_string_to_matrix("[2, -2/3, 2; 2, -1/3, -1; 1, 0, -2; 0, 2/3, 3/2; ]")

        self._seqs = tk.IntVar(self, starting_matrix.shape[1] - 1)
        self._exprs = tk.IntVar(self, starting_matrix.shape[0])
        self._merge_expressions_opt = tk.IntVar(self, 1)
        self._simplify_results_opt = tk.IntVar(self, 0)

        self._proposed_latex = ''
        self._proposed_latex_full = ''
        self._result_latex = "Result not generated."

        title_Hframe = tk.Frame(self)
        title_Hframe.pack(side=tk.TOP, expand=True, fill=tk.X)

        title_text = tk.Label(title_Hframe, text="Automatic inequality Solver")
        title_text.pack(side=tk.LEFT)

        user_input_Hframe = tk.Frame(self)
        user_input_Hframe.pack(side=tk.TOP, fill=tk.X)

        self._ineq_grid_frame_scrollable = ScrollableFrame(user_input_Hframe, x_scrollable=True, y_scrollable=True)
        self._ineq_grid_frame_scrollable.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._ineq_grid_scrollable_interior = self._ineq_grid_frame_scrollable.get_inner_frame()

        self._ineq_grid_frame = IneqGrid(self._ineq_grid_scrollable_interior, self._exprs.get(), self._seqs.get())
        self._ineq_grid_frame.pack(side=tk.LEFT)

        # These two listen for changes in the problem size. The latter is more complex and resizes the IneqGrid canvas
        self._exprs.trace('w', lambda *args: self._ineq_grid_frame.adjust_cols(self._exprs.get()))
        self._seqs.trace('w', lambda *args: self._change_num_rows(self._seqs.get()))

        # user_input_Hframe
        user_settings_Hframe = tk.Frame(user_input_Hframe)
        user_settings_Hframe.pack(side=tk.RIGHT, expand=False, fill=tk.Y)

        very_left_settings_Vframe = tk.Frame(user_settings_Hframe, padx=4)
        very_left_settings_Vframe.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        very_left_settings_row1_Hframe = tk.Frame(very_left_settings_Vframe, padx=2)
        very_left_settings_row1_Hframe.pack(side=tk.TOP)

        very_left_settings_row2_Hframe = tk.Frame(very_left_settings_Vframe, padx=2)
        very_left_settings_row2_Hframe.pack(side=tk.TOP)

        matrix_buttons = []
        for i in range(0, 3):
            matrix_buttons.append(tk.Button(very_left_settings_row1_Hframe, text=chr(ord('A')+i),
                                            command=lambda d=i: self._use_example_mtx(d), width=1))
        for i in range(3, 6):
            matrix_buttons.append(tk.Button(very_left_settings_row2_Hframe, text=chr(ord('A')+i),
                                            command=lambda d=i: self._use_example_mtx(d), width=1))

        for m_b in matrix_buttons:
            m_b.pack(side=tk.LEFT)

        clear_mtx_button = tk.Button(very_left_settings_Vframe, text="Clear", command=self._clear_input_matrix)
        clear_mtx_button.pack(side=tk.TOP, fill=tk.X, padx=2)

        left_settings_Vframe = tk.Frame(user_settings_Hframe, padx=4)
        left_settings_Vframe.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        copy_paste_ineq_Hframe = tk.Frame(left_settings_Vframe)
        copy_paste_ineq_Hframe.pack(side=tk.TOP, fill=tk.X)

        copy_ineq_mtx_button = tk.Button(copy_paste_ineq_Hframe, text="Copy", command=self._copy_proposed_mtx)
        copy_ineq_mtx_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        paste_ineq_mtx_button = tk.Button(copy_paste_ineq_Hframe, text="Paste", command=self._paste_proposed_mtx)
        paste_ineq_mtx_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        change_mtx_size_Vframe = tk.Frame(left_settings_Vframe, pady=2)
        change_mtx_size_Vframe.pack(side=tk.TOP)

        self._dim_changer_dim = DimChanger(change_mtx_size_Vframe, desc_text="Expressions:",
                                           modifying_var=self._exprs, min_val=my_constants.EXPRS_MIN, max_val=my_constants.EXPRS_MAX)
        self._dim_changer_dim.pack(side=tk.TOP, expand=True, fill=tk.X)

        self._dim_changer_seqs = DimChanger(change_mtx_size_Vframe, desc_text="Sequences:",
                                      modifying_var=self._seqs, min_val=my_constants.SEQS_MIN, max_val=my_constants.SEQS_MAX)
        self._dim_changer_seqs.pack(side=tk.TOP, expand=True, fill=tk.X)

        right_settings_Vframe = tk.Frame(user_settings_Hframe, width=16)
        right_settings_Vframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        simplifications_Vframe = tk.Frame(right_settings_Vframe)
        simplifications_Vframe.pack(side=tk.TOP, fill=tk.X)

        merge_expressions_frame = tk.Frame(simplifications_Vframe)
        merge_expressions_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        merge_expressions_checkbox = tk.Checkbutton(merge_expressions_frame, text="Merge expressions",
                                                    variable=self._merge_expressions_opt)
        merge_expressions_checkbox.pack(side=tk.LEFT, fill=tk.X)

        simplify_results_frame = tk.Frame(simplifications_Vframe)
        simplify_results_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        simplify_results_checkbox = tk.Checkbutton(simplify_results_frame, text="Simplify expressions",
                                                   variable=self._simplify_results_opt)
        simplify_results_checkbox.pack(side=tk.LEFT)

        run_button = tk.Button(right_settings_Vframe, text='Run', command=self._run_button_pressed, width=10)
        run_button.pack(side=tk.BOTTOM)

        self._ineq_in_render = IneqInRender(self, text="You've asked about the inequality:")
        self._ineq_in_render.pack(side=tk.TOP, expand=False, fill=tk.X)

        bottom_Hframe = tk.Frame(self)
        bottom_Hframe.pack(side=tk.BOTTOM, expand=True, fill=tk.X)

        copy_in_ineq_button = tk.Button(bottom_Hframe, text="Copy Proposed Inequality",
                                        command=self._copy_proposed_latex)
        copy_in_ineq_button.pack(side=tk.LEFT)

        copy_out_ineq_button = tk.Button(bottom_Hframe, text="Copy Inequality Decomposition",
                                         command=self._copy_out_latex)
        copy_out_ineq_button.pack(side=tk.LEFT, padx=2)

        copy_layex_imports_button = tk.Button(bottom_Hframe, text="Copy LaTeX Imports",
                                         command=self._copy_latex_imports)
        copy_layex_imports_button.pack(side=tk.LEFT, padx=2)

        self._error_message_frame = UserMessage(bottom_Hframe)
        self._error_message_frame.pack(side=tk.RIGHT, padx=2, expand=True, fill=tk.BOTH)

        result_Hframe = tk.Frame(self, pady=4)
        result_Hframe.pack(side=tk.TOP, expand=True, fill=tk.X)

        self._ineqs_out_Vframe = tk.LabelFrame(result_Hframe, text="Please press 'run'")
        self._ineqs_out_Vframe.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        _ineqs_out_Vframe_scrollable = ScrollableFrame(self._ineqs_out_Vframe, start_width=420,
                                                       x_scrollable=True, y_scrollable=True)
        _ineqs_out_Vframe_scrollable.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._ineqs_out_Vframe_inner = _ineqs_out_Vframe_scrollable.get_inner_frame()

        self._holder_decomp_frame = DecompIneqFrame(self._ineqs_out_Vframe_inner, "Hölder",
                                                    self._holder_ineq_hovered, self._ineq_unhovered,
                                                    self._holder_ineq_clicked)
        self._holder_decomp_frame.pack(side=tk.TOP, fill=tk.X)
        self._lp_mon_decomp_frame = DecompIneqFrame(self._ineqs_out_Vframe_inner, "Lp monotonicity",
                                                    self._lp_mon_ineq_hovered, self._ineq_unhovered,
                                                    self._lp_mon_ineq_clicked)
        self._lp_mon_decomp_frame.pack(side=tk.TOP, fill=tk.X)

        self._visual_out_frame = GraphOut(result_Hframe, text="This can be visualised as:")
        self._visual_out_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Run the solver on starting matrix
        self._ineq_grid_frame.set_value(starting_matrix)
        self._run_button_pressed()

    def _show_message(self, message, is_error_message=False):
        if is_error_message:
            self._error_message_frame.error_message(message)
        else:
            self._error_message_frame.normal_message(message)

    def _change_num_rows(self, new_num):
        self._ineq_grid_frame.adjust_rows(new_num)
        if new_num <= 4:
            self._ineq_grid_frame_scrollable.change_height(27+19*new_num)
        else:
            self._ineq_grid_frame_scrollable.change_height(27+19*4)

    def _change_to_mtx(self, m):
        self._dim_changer_dim.set_val(f"{m.shape[0]}")
        self._dim_changer_seqs.set_val(f"{m.shape[1] - 1}")
        self._ineq_grid_frame.set_value(m)

    def _use_example_mtx(self, i):
        matrices = [
            "[2, -2/3, 2; 2, -1/3, -1; 1, 0, -2; 0, 2/3, 3/2; ]",
            "[2, -2/3, 2; 2, -1/3, -1; 1, 0, -2; 0, 2/3, 3/2; 2, -2/3, 2; 2, -1/3, -1; 1, 0, -2; 0, 2/3, 3/2; 1, 0, "
            "1/2; 0, 1, 1/2; 1/2, 1/2, -1; ]",
            "[3, 0, 0, 1; 0, 3, 0, 1; 0, 0, 3, 1; 1, 1, 1, -3; ]",
            "[0, -4, 1/2; 0, -4, 1/2; 0, -4, -1;]",
            "[-5/3, 5/3, 1/5; 5/4, 0, 4/5; 2/3, 1/3, -1;3/4, -3/2, 2/3; -2, 0, 1/3; -1/6, -1, -1;-1, -1, 1/4; "
            "4/9, -2/3, 3/4; 1/12, -3/4, -1;0, -4/3, 1/2; 0, 0, 1/2; 0, -2/3, -1;0, 1/2, 1/2; 0, 2, 1/2; 0, 5/4, -1;"
            "-2, 2/3, 1/2; 0, -4/3, 1/2; -1, -1/3, -1;-3/2, 1/2, 2/3; -2, -1, 1/3; -5/3, 0, -1;]",
            "[0, 1/2, 0, 2, 1, 0, -1, 2/3, -2, 0, 0, 1, 1/2; 1, 1, 1, -2/3, 1, 0, 0, -2, 1/2, 0, 0, 1, 1/2; "
            "1/2, 3/4, 1/2, 2/3, 1, 0, -1/2, -2/3, -3/4, 0, 0, 1, -1; 0, 2, 0, -1/2, 0, 0, 0, 1, 1/2, 0, 2/3, -1, 1/2; "
            "-2, -1, -4/3, 0, 0, 1, -1/2, 0, -2/3, 0, 1/2, 2/3, 1/2; "
            "-1, 1/2, -2/3, -1/4, 0, 1/2, -1/4, 1/2, -1/12, 0, 7/12, -1/6, -1; "
            "0, 0, -1, 1, 0, 0, -2, -2/3, -4/3, -1/2, -1/2, -1, 1/2; "
            "2, -4/3, -1, -1/2, 0, -1/2, 1, 0, 4/3, 0, 0, 2, 1/2; "
            "1, -2/3, -1, 1/4, 0, -1/4, -1/2, -1/3, 0, -1/4, -1/4, 1/2, -1; ]"
        ]
        m = matlab_matrix_string_to_matrix(matrices[i])
        self._change_to_mtx(m)

    def _clear_input_matrix(self):
        m = np.full([self._exprs.get(), self._seqs.get()+1], "", dtype=object)
        self._change_to_mtx(m)

    def _copy_proposed_mtx(self):
        pyperclip.copy(matrix_to_matlab_matrix_string(self._ineq_grid_frame.get_str_value()))
        self._show_message("Copied proposed matrix!", False)

    def _paste_proposed_mtx(self):
        m = None
        success_pasting = False
        try:
            m = matlab_matrix_string_to_matrix(pyperclip.paste())
            success_pasting = True
        except ValueError as e:
            self._show_message(str(e), True)
        if m is not None and success_pasting:
            if m.shape[0] <= my_constants.EXPRS_MAX and m.shape[1] <= my_constants.SEQS_MAX:
                self._show_message("Pasted!", False)
                self._change_to_mtx(m)
            else:
                self._show_message(f"Matrix must be at most {my_constants.EXPRS_MAX}x{my_constants.SEQS_MAX}!", True)

    def _copy_proposed_latex(self):
        pyperclip.copy(self._proposed_latex_full)
        self._show_message("Copied proposed inequality!", False)

    def _copy_out_latex(self):
        pyperclip.copy(self._result_latex)
        self._show_message("Copied inequality decomposition!", False)

    def _copy_latex_imports(self):
        s = r"\usepackage{amsmath}"
        pyperclip.copy(s)
        self._show_message("Copied imports!", False)

    def _holder_ineq_hovered(self, eqn_index):
        if self._allow_graphic_interaction:
            self._visual_out_frame.preview_holder(eqn_index)

    def _lp_mon_ineq_hovered(self, eqn_index):
        if self._allow_graphic_interaction:
            self._visual_out_frame.preview_lp_mon(eqn_index)

    def _ineq_unhovered(self):
        if self._allow_graphic_interaction:
            self._visual_out_frame.cancel_preview()

    def _holder_ineq_clicked(self, eqn_index):
        if self._allow_graphic_interaction:
            self._visual_out_frame.holder_ineq_clicked(eqn_index)

    def _lp_mon_ineq_clicked(self, eqn_index):
        if self._allow_graphic_interaction:
            self._visual_out_frame.lp_mon_ineq_clicked(eqn_index)

    def _run_button_pressed(self):
        if self._ineq_grid_frame.get_matrix_validity():
            inA = self._ineq_grid_frame.get_value()
            num_dims = inA.shape[1]-1  # should be equivalent to self._seqs.get()
            if num_dims == 2:
                self._visual_out_frame.change_title_text("This can be visualised as:")
                self._allow_graphic_interaction = True
            else:
                self._visual_out_frame.change_title_text("Sequences=2 required for visualisation")
                self._allow_graphic_interaction = False

            if self._merge_expressions_opt.get():
                inA = vvip.merge_common_matrix_expressions(inA)

            self._proposed_latex = vvip.get_latex(inA, mode='inline', include_geq=True,
                                                  simplify=self._simplify_results_opt.get())
            self._proposed_latex_full = vvip.get_latex(inA, mode='full', include_geq=True,
                                                       simplify=self._simplify_results_opt.get())
            self._ineq_in_render.replace_text(self._proposed_latex)

            if not self._merge_expressions_opt.get():  # if not already merged
                inA = vvip.merge_common_matrix_expressions(inA)

            self._visual_out_frame.set_initial_points(inA)

            res = vvip.ineq_solver(inA, merge_common_expressions=False)

            # delete objects if not already
            if res.eq_valid:
                num_inequalities = res.holder_ineqs_overall_powers.shape[0]+ res.lp_mon_ineqs_overall_powers.shape[0]
                if num_inequalities == 0:
                    self._ineqs_out_Vframe.configure(text="Your inequality is trivially true.")
                else:
                    self._ineqs_out_Vframe.configure(text="Your inequality can be decomposed as:")

                self._holder_decomp_frame.set(res.holder_ineqs_matrix, res.holder_ineqs_overall_powers,
                                              self._simplify_results_opt.get())
                self._lp_mon_decomp_frame.set(res.lp_mon_ineqs_matrix, res.lp_mon_ineqs_overall_powers,
                                              self._simplify_results_opt.get())

                self._visual_out_frame.set_possible_moves(res.holder_ineqs_matrix, res.holder_ineqs_overall_powers,
                                                          res.lp_mon_ineqs_matrix, res.lp_mon_ineqs_overall_powers)
                self._result_latex = decomp_to_latex(res.holder_ineqs_matrix, res.holder_ineqs_overall_powers,
                                                     res.lp_mon_ineqs_matrix, res.lp_mon_ineqs_overall_powers,
                                                     self._simplify_results_opt.get())
            else:
                self._ineqs_out_Vframe.configure(text="Your inequality is false.")
                self._result_latex = 'The proposed inequality is false.'
                self._holder_decomp_frame.clear()
                self._lp_mon_decomp_frame.clear()

        else:
            self._show_message("Couldn't run: matrix is invalid!", True)


def run_gui(minx=656, miny=480):
    root = tk.Tk()
    root.bind_all('<Button>', lambda event: event.widget.focus_set())  # allow deselection of widgets

    gui_Vframe = _GUI(root)
    gui_Vframe.pack(expand=True, fill=tk.BOTH, padx=6, pady=(4, 10))

    root.geometry("800x600")
    root.minsize(minx, miny)
    root.title("Automatic Inequality Solver")
    root.mainloop()


if __name__ == '__main__':
    run_gui()

