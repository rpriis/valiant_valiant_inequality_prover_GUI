
import constants as my_constants
from helper_funcs import is_float_val

import tkinter as tk
import numpy as np


class IneqGridCell(tk.Entry):
    def __init__(self, parent, is_power_cell):
        self._string_var = tk.StringVar()
        self._string_var.trace('w', self._check_val)
        self._string_value = ""

        super().__init__(parent, width=6, textvariable=self._string_var)
        if is_power_cell:
            self.pack(side=tk.LEFT)
        else:
            self.pack(side=tk.TOP)

        self._set_validity(False)

    def set_value(self, val):
        self.delete(0, tk.END)
        self.insert(0, f"{val}")

    def get_value(self):
        return self._value

    def get_str_value(self):
        return self._string_value

    def get_cell_validity(self):
        return self._input_is_valid

    def _set_validity(self, validity):
        if validity:
            self.config(bg='white')
            self._input_is_valid = True  # !!! maybe declare this variable earlier
        else:
            self.config(bg='#FFB0B0')
            self._input_is_valid = False

    def _check_val(self, *_):
        val = self._string_var.get()
        a = val.split("/")

        if not is_float_val(a[0]):
            pass
        elif len(a) == 1:
            self._value = np.float64(a[0])
            self._string_value = val
            self._set_validity(True)
            return
        elif len(a) == 2 and is_float_val(a[1]):
            v2 = np.float64(a[1])
            if v2 > my_constants.ZERO_BOUND:  # avoid division by zero. Also disallows negative numbers in the denom.
                self._value = np.float64(a[0])/np.float64(a[1])
                self._string_value = val
                self._set_validity(True)
                return

        self._set_validity(False)


class IneqGridColumn(tk.Frame):
    def __init__(self, parent, num_seqs):
        super().__init__(parent)
        self._cells = [IneqGridCell(self, is_power_cell=False) for _ in range(num_seqs)]
        self.pack(side=tk.LEFT)

    def set_value(self, vals):
        for i in range(len(vals)):
            self._cells[i].set_value(vals[i])

    def add_row(self):
        self._cells.append(IneqGridCell(self, is_power_cell=False))

    def remove_row(self):
        self._cells[-1].destroy()
        self._cells.pop()

    def get_col_validity(self):
        return all([c.get_cell_validity() for c in self._cells])

    def get_col_values(self):
        return [self._cells[i].get_value() for i in range(len(self._cells))]

    def get_col_str_values(self):
        return [self._cells[i].get_str_value() for i in range(len(self._cells))]


class IneqGrid(tk.Frame):
    def __init__(self, parent, num_exprs, num_seqs):
        super().__init__(parent)
        self._current_num_cols = num_exprs
        self._current_num_rows = num_seqs

        self._ineq_grid_input_Hframe = tk.LabelFrame(self)
        self._ineq_grid_input_Hframe.pack(side=tk.TOP)

        self._columns = [IneqGridColumn(self._ineq_grid_input_Hframe, num_seqs) for _ in range(self._current_num_cols)]

        self._ineq_powers_input_Hframe = tk.LabelFrame(self)
        self._ineq_powers_input_Hframe.pack(side=tk.TOP)
        self._powers = [
            IneqGridCell(self._ineq_powers_input_Hframe, is_power_cell=True) for _ in range(self._current_num_cols)
        ]

    def set_value(self, m):
        for i in range(self._current_num_cols):
            self._columns[i].set_value(m[i, :-1])
            self._powers[i].set_value(m[i, -1])

    def get_matrix_validity(self):
        return all([c.get_col_validity() for c in self._columns]) and all([p.get_cell_validity() for p in self._powers])

    def get_value(self):
        matrix_val = np.empty((self._current_num_cols, self._current_num_rows+1))
        for i in range(self._current_num_cols):
            col_vals = self._columns[i].get_col_values()
            col_vals.append(self._powers[i].get_value())
            matrix_val[i] = np.asarray(col_vals, dtype=np.float64)
        return matrix_val

    def get_str_value(self):
        matrix_val = np.empty((self._current_num_cols, self._current_num_rows + 1), dtype=object)
        for i in range(self._current_num_cols):
            col_vals = self._columns[i].get_col_str_values()
            col_vals.append(self._powers[i].get_str_value())
            matrix_val[i] = np.asarray(col_vals)
        return matrix_val

    def adjust_cols(self, new_num_cols):
        if self._current_num_cols > new_num_cols:
            for _ in range(self._current_num_cols - new_num_cols):
                self._remove_column()
        elif self._current_num_cols < new_num_cols:
            for _ in range(new_num_cols - self._current_num_cols):
                self._add_column()

        self._current_num_cols = new_num_cols

    def _add_column(self):
        self._columns.append(IneqGridColumn(self._ineq_grid_input_Hframe, self._current_num_rows))
        self._powers.append(IneqGridCell(self._ineq_powers_input_Hframe, is_power_cell=True))

    def _remove_column(self):
        self._columns[-1].destroy()
        self._columns.pop()
        self._powers[-1].destroy()
        self._powers.pop()

    def adjust_rows(self, new_num_rows):
        if self._current_num_rows > new_num_rows:
            for _ in range(self._current_num_rows - new_num_rows):
                self._remove_row()
        elif self._current_num_rows < new_num_rows:
            for _ in range(new_num_rows - self._current_num_rows):
                self._add_row()

        self._current_num_rows = new_num_rows

    def _add_row(self):
        for c in self._columns:
            c.add_row()

    def _remove_row(self):
        for c in self._columns:
            c.remove_row()


