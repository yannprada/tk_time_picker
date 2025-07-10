import tkinter as tk
from dataclasses import dataclass
from PIL import Image, ImageTk


@dataclass
class TimePicker(tk.Frame):
    master: tk.Widget
    hours_limit: float = 23
    
    def __post_init__(self):
        super().__init__(self.master)
        
        inner = tk.Frame(self)
        inner.pack(padx=5, pady=5)
        
        self._hours = UnitPicker(inner, maxi=self.hours_limit, increment2=3)
        self._minutes = UnitPicker(inner)
        self._seconds = UnitPicker(inner)
        
        self._hours.pack(side='left')
        tk.Label(inner, text=':').pack(side='left')
        self._minutes.pack(side='left')
        tk.Label(inner, text=':').pack(side='left')
        self._seconds.pack(side='left')
        
        self._minutes.bind('<<OnWrapDown>>', lambda event: self._hours.add(-1))
        self._minutes.bind('<<OnWrapUp>>', lambda event: self._hours.add(1))
        self._seconds.bind('<<OnWrapDown>>', lambda event: self._minutes.add(-1))
        self._seconds.bind('<<OnWrapUp>>', lambda event: self._minutes.add(1))
    
    def __str__(self):
        return f'{self._hours}:{self._minutes}:{self._seconds}'


@dataclass
class UnitPicker(tk.Frame):
    master: tk.Widget
    maxi: int = 59
    increment: int = 1
    increment2: int = 5
    
    def __post_init__(self):
        super().__init__(self.master)
        
        self.value = 0
        self.tk_value = tk.StringVar(value='00')
        
        label = tk.Label(self, textvariable=self.tk_value, font=['', 12])
        label.grid(row=1, column=0, columnspan=2)
        
        self.imgs = list(map(lambda src: ImageTk.PhotoImage(Image.open(src)), 
                             ['up2.png', 'up.png', 'down2.png', 'down.png']))
        self._add_button(self.imgs[0], self.increment2, row=0, column=0)
        self._add_button(self.imgs[1], self.increment, row=0, column=1)
        self._add_button(self.imgs[2], -self.increment2, row=2, column=0)
        self._add_button(self.imgs[3], -self.increment, row=2, column=1)
    
    def _add_button(self, img, increment, row, column):
        button = tk.Button(self, image=img, command=lambda: self.add(increment))
        button.grid(row=row, column=column)
    
    def add(self, amount):
        new_value = self.value + amount
        
        if new_value < 0:
            self.value = self.maxi + new_value + 1
            self.event_generate('<<OnWrapDown>>')
        elif new_value > self.maxi:
            self.value = new_value - self.maxi - 1
            self.event_generate('<<OnWrapUp>>')
        else:
            self.value = new_value
        
        self.tk_value.set(f'{self.value:02d}')
    
    def __str__(self):
        return self.tk_value.get()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TimePicker testing')
    root.geometry('300x300+1000+200')
    root.configure(bg='grey')
    TimePicker(root).pack()
    TimePicker(root, 99).pack()
    # UnitPicker(root).pack()
    # UnitPicker(root, maxi=23, increment2=3).pack()
    root.mainloop()