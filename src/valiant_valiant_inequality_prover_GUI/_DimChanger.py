
import constants as my_constants

import tkinter as tk


class DimChanger(tk.Frame):
    def __init__(self, parent, desc_text, modifying_var, min_val, max_val):
        super().__init__(parent)
        self._modifying_var = modifying_var
        self._min_val = min_val
        self._max_val = max_val
        self._spinbox = tk.Spinbox(self, from_=min_val, to=max_val, width=4, validate='focusout',
                                   validatecommand=(self.register(self._spinbox_validate), '%P')
                                   )
        # workaround because default value is 1; when deleting
        self._spinbox.insert(0, self._modifying_var.get())
        self._spinbox.delete(len(str(self._modifying_var.get())), 'end')
        self._spinbox.pack(side=tk.RIGHT)

        self._desc_label = tk.Label(self, text=desc_text)
        self._desc_label.pack(side=tk.RIGHT)

        self._spinbox.bind('<Return>', lambda x: parent.focus())

    def _spinbox_validate(self, proposed_val):
        if proposed_val.isdigit():
            proposed_int = int(proposed_val)
            if self._min_val <= proposed_int <= self._max_val:
                if hasattr(self, '_spinbox'):  # tk.Spinbox() calls validatecommand before returning
                    self._spinbox.config(bg='white')
                    self._modifying_var.set(proposed_int)
                return True
        if hasattr(self, '_spinbox'):  # tk.Spinbox() calls validatecommand before returning
            self._spinbox.config(bg=my_constants.ERROR_HIGHLIGHT_COLOUR)
        return False

    def set_val(self, new_val):
        if self._spinbox_validate(new_val):
            self._spinbox.insert(0, self._modifying_var.get())
            self._spinbox.delete(len(str(self._modifying_var.get())), 'end')


