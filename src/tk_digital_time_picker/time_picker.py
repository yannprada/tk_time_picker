import tkinter as tk
from dataclasses import dataclass, field


def _get_time_string(obj):
    return f'{obj.hours:02d}:{obj.minutes:02d}:{obj.seconds:02d}'


@dataclass
class TimePicker(tk.Button):
    master: tk.Widget
    hours_limit: float = 24
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    
    def __post_init__(self):
        super().__init__(self.master)
        self._display_value = tk.StringVar()
        self.configure(textvariable=self._display_value, command=self.on_press)
    
    def __setattr__(self, name, value):
        if (name == 'seconds'):
            self.minutes += value // 60
            value = value % 60

        if (name == 'minutes'):
            self.hours += value // 60
            value = value % 60

        if (name == 'hours'):
            value = value % self.hours_limit

        super(self.__class__, self).__setattr__(name, value)
        self._update_display()

    def _update_display(self):
        if hasattr(self, '_display_value'):
            self._display_value.set(
                f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}')

    def on_press(self):
        dialog = TimePickerDialog(self, self.hours_limit, self.hours, 
                                  self.minutes, self.seconds)
        self.wait_window(dialog.root)
        self.hours = dialog.hours
        self.minutes = dialog.minutes
        self.seconds = dialog.seconds
        self._update_display()

    def __str__(self):
        return self._display_value.get()

    def get_seconds(self):
        return self.hours * 3600 + self.minutes * 60 + self.seconds
    
    def set_value(self, value):
        if type(value) not in [str, list, tuple]:
            raise TypeError(f'TimePicker.set_value accepts a string, list or '
                            f'tuple, got {type(value)}')

        if type(value) is str:
            value = value.split(':')
        
        if len(value) != 3:
            raise AttributeError(f'TimePicker.set_value should contain 3 '
                                 f'values, got {len(value)}')
        
        self.hours = int(value[0])
        self.minutes = int(value[1])
        self.seconds = int(value[2])


@dataclass
class TimePickerDialog:
    master: tk.Widget
    hours_limit: float = 24
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    font_size: int = 20

    def __post_init__(self):
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()

        self.root = tk.Toplevel(self.master)
        # place on top of the TimePicker
        self.root.geometry(f'300x200+{x}+{y}')
        self.root.title('Pick a time')

        top = tk.Frame(self.root)
        top.pack(fill='both', expand=True)

        inner = tk.Frame(top)
        inner.pack(pady=20)

        self._hours = UnitPicker(inner, value=self.hours, font_size=self.font_size, 
                                 maxi=self.hours_limit, increment2=3)
        self._minutes = UnitPicker(inner, value=self.minutes, font_size=self.font_size)
        self._seconds = UnitPicker(inner, value=self.seconds, font_size=self.font_size)
        
        self._hours.pack(side='left')
        tk.Label(inner, text=':', font=['', self.font_size]).pack(side='left')
        self._minutes.pack(side='left')
        tk.Label(inner, text=':', font=['', self.font_size]).pack(side='left')
        self._seconds.pack(side='left')
        
        self._minutes.bind('<<OnWrapDown>>', lambda event: self._hours.add(-1))
        self._minutes.bind('<<OnWrapUp>>', lambda event: self._hours.add(1))
        self._seconds.bind('<<OnWrapDown>>', lambda event: self._minutes.add(-1))
        self._seconds.bind('<<OnWrapUp>>', lambda event: self._minutes.add(1))

        bottom = tk.Frame(self.root)
        bottom.pack(pady=20)

        cancel = tk.Button(bottom, text='Cancel', command=self.root.destroy, font=['', 12])
        cancel.pack(side='left')
        ok = tk.Button(bottom, text='OK', command=self.ok, font=['', 12])
        ok.pack(side='left')

        self.root.grab_set()

    def ok(self):
        self.hours = self._hours.value
        self.minutes = self._minutes.value
        self.seconds = self._seconds.value
        self.root.grab_release()
        self.root.destroy()


@dataclass
class UnitPicker(tk.Frame):
    master: tk.Widget
    maxi: int = 60
    increment: int = 1
    increment2: int = 5
    value: int = 0
    font_size: int = 20
    
    def __post_init__(self):
        super().__init__(self.master)
        
        self.tk_value = tk.StringVar(value='00')
        
        top = tk.Frame(self)
        bottom = tk.Frame(self)
        label = tk.Label(self, textvariable=self.tk_value, font=['', self.font_size])
        
        top.pack()
        label.pack()
        bottom.pack()
        
        self.buttons = []
        self._add_button('🠝🠝', self.increment2, top)
        self._add_button('🠝', self.increment, top, 1)
        self._add_button('🠟🠟', -self.increment2, bottom)
        self._add_button('🠟', -self.increment, bottom, 1)

        self._update()
    
    def _add_button(self, symbol, increment, parent, column=0):
        button = tk.Button(parent, text=symbol, command=lambda: self.add(increment))
        button.grid(row=0, column=column)
        self.buttons.append(button)
    
    def add(self, amount):
        new_value = self.value + amount
        
        if new_value < 0:
            self.value = self.maxi + new_value
            self.event_generate('<<OnWrapDown>>')
        elif new_value >= self.maxi:
            self.value = new_value - self.maxi
            self.event_generate('<<OnWrapUp>>')
        else:
            self.value = new_value
        
        self._update()
    
    def _update(self):
        self.tk_value.set(f'{self.value:02d}')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TimePicker testing')
    root.geometry('300x300+1000+200')
    root.configure(bg='grey')
    TimePicker(root).pack()
    TimePicker(root, hours_limit=99).pack()
    root.mainloop()