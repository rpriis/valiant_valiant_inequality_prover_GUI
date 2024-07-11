

import valiant_valiant_inequality_prover.prover as vvip

import numpy as np


def matrix_to_matlab_matrix_string(m):
    if m.ndim != 2:
        raise ValueError("Error: provided matrix should be 2-dimensional")

    out_str = "["
    for i in range(m.shape[0]):
        for j in range(m.shape[1]-1):
            out_str += f"{m[i, j]}, "
        out_str += f"{m[i, -1]}; "
    return out_str + "]"


def matlab_matrix_string_to_matrix(in_str):
    if in_str is None:
        raise ValueError("Invalid input string: is None")
    in_str = in_str.replace(' ', '').replace('\n', '')
    if len(in_str) == 0:
        raise ValueError("Invalid input string: is empty")
    if in_str[0] != '[' or in_str[-1] != ']':
        raise ValueError("Invalid input string.")

    in_str = in_str[1:-1]
    rows = in_str.split(";")
    num_rows = len(rows)
    for i in range(num_rows):
        if rows[i] == '':
            rows.pop(i)
            num_rows -= 1
    if num_rows == 0:
        raise ValueError("Invalid input string.")
    row_length = len(rows[0].split(','))
    if row_length < 2:
        raise ValueError("Invalid input string.")

    out_arr = np.empty((num_rows, row_length), dtype=object)
    for i in range(num_rows):
        col_vals = rows[i].split(',')
        if len(col_vals) != row_length:
            raise ValueError(f"Invalid input string.")
        for j in range(row_length):
            out_arr[i, j] = col_vals[j]
    return out_arr


def decomp_to_latex(holder_moves, holder_powers, lp_mon_moves, lp_mon_powers, simplify):
    num_holder, num_lp_mon = len(holder_powers), len(lp_mon_powers)
    holder_ineqs = holder_moves.copy()
    holder_ineqs[:, :, -1] *= -1
    lp_mon_ineqs = lp_mon_moves.copy()
    lp_mon_ineqs[:, :, -1] *= -1

    if num_holder + num_lp_mon == 0:
        return 'Your inequality can be decomposed as a product of (solely) trivial inequalities.'
    s = ''

    if num_holder > 0:
        s += (f"{num_holder} " + r'H\"{o}lder Inequalit' + ('y' if num_holder == 1 else 'ies') +
              r':\begin{equation*}\begin{split}')
        x = [vvip.get_latex(holder_ineqs[i], mode='raw', include_geq=False, simplify=simplify) for i in
             range(num_holder)]
        for i in range(num_holder):
            s += r'\left[' + x[i] + r'\right]^{' + '%3.3g' % holder_powers[i] + r'}&\geq1\\' + '\n'
        s += r'\end{split}\end{equation*}'

    if num_lp_mon > 0:
        if num_holder > 0:
            s += "and "
        s += (f"{num_lp_mon} $L_p$ Monotonicity Inequalit" + ('y' if num_lp_mon == 1 else 'ies') +
              r':\begin{equation*}\begin{split}')
        x = [vvip.get_latex(lp_mon_ineqs[i], mode='raw', include_geq=False, simplify=simplify) for i in
             range(num_lp_mon)]
        for i in range(num_lp_mon):
            s += r'\left[' + x[i] + r'\right]^{' + '%3.3g' % lp_mon_powers[i] + r'}&\geq1\\' + '\n'
        s += r'\end{split}\end{equation*}'

    return s


def is_float_val(val):
    if val is None or len(val) == 0:
        return False
    if val[0] == '-':  # ignore leading minus
        val = val[1:]
    if val.count('.') > 1:  # (this is faster than splitting into array and getting length)
        return False

    a = val.split('.')
    return len(a[0]) > 0 and a[0].isnumeric() and (len(a[1]) > 0 and a[1].isnumeric() if len(a) > 1 else True)


def apply_negative_matrix_powers(m, powers):
    t = m.T
    t[-1, :, :] *= -powers
    return t.T
