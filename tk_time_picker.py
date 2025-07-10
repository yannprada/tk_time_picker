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
        self._seconds.bind('<<OnWrapDown>>', lambda event: self._minutes.add(-1))
        self._minutes.bind('<<OnWrapUp>>', lambda event: self._hours.add(1))
        self._seconds.bind('<<OnWrapUp>>', lambda event: self._minutes.add(1))


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
        
        self.option_add('*Label*font', ['', 12])
        self._up = ImageTk.PhotoImage(Image.open("up.png"), (20, 10))
        self._up2 = ImageTk.PhotoImage(Image.open("up2.png"), (20, 10))
        self._down = ImageTk.PhotoImage(Image.open("down.png"), (20, 10))
        self._down2 = ImageTk.PhotoImage(Image.open("down2.png"), (20, 10))
        
        tk.Button(self, image=self._up2, command=lambda: self.add(self.increment2)).grid(row=0, column=0)
        tk.Button(self, image=self._up, command=lambda: self.add(self.increment)).grid(row=0, column=1)
        
        tk.Label(self, textvariable=self.tk_value).grid(row=1, column=0, columnspan=2)
        
        tk.Button(self, image=self._down2, command=lambda: self.add(-self.increment2)).grid(row=2, column=0)
        tk.Button(self, image=self._down, command=lambda: self.add(-self.increment)).grid(row=2, column=1)
    
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