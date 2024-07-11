
import tkinter as tk


class UserMessage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._error_text_label = tk.Label(self, text="")
        self._error_text_label.pack(side=tk.RIGHT)
        self._t = 0

        self._new_message = ""

        self._active_timers = []

    def error_message(self, message):
        self._clear_active_timers()
        self._new_message = message
        self._error_flash_in()
        self._active_timers.append(self.after(80, self._flash_out))
        self._active_timers.append(self.after(140, self._error_flash_in))
        self._active_timers.append(self.after(6000, self._error_fade_out))

    def normal_message(self, message):
        self._clear_active_timers()
        self._new_message = message
        self._normal_flash_in()
        self._active_timers.append(self.after(80, self._flash_out))
        self._active_timers.append(self.after(140, self._normal_flash_in))
        self._active_timers.append(self.after(4000, self._normal_fade_out))

    def _clear_active_timers(self):
        for t in self._active_timers:
            self.after_cancel(t)
        self._active_timers = []

    def _error_flash_in(self):
        self._error_text_label.config(foreground="red")
        self._error_text_label.config(text=self._new_message)

    def _normal_flash_in(self):
        self._error_text_label.config(foreground="black")
        self._error_text_label.config(text=self._new_message)

    def _flash_out(self):
        self._error_text_label.config(text="")
        self._error_text_label.config(foreground="black")

    def _error_fade_out(self):
        colour_result = max(self._t*2, 0)**1.4
        if colour_result < 250:
            str_colour1 = f"{int(colour_result):02x}"
            self._error_text_label.config(foreground="#FF"+str_colour1*2)
            self._active_timers.append(self.after(60, self._error_fade_out))
            self._t += 1
        else:
            self._error_text_label.config(text="")
            self._error_text_label.config(foreground="black")
            self._t = 0

    def _normal_fade_out(self):
        colour_result = max(self._t*2, 0)**1.4
        if colour_result < 250:
            str_colour1 = f"{int(colour_result):02x}"
            self._error_text_label.config(foreground="#"+str_colour1*3)
            self._active_timers.append(self.after(60, self._normal_fade_out))
            self._t += 1
        else:
            self._error_text_label.config(text="")
            self._error_text_label.config(foreground="black")
            self._t = 0

