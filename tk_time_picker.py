import tkinter as tk
from dataclasses import dataclass
from PIL import Image, ImageTk


@dataclass
class TimePicker(tk.Frame):
    master: tk.Widget
    hours_limit: float = 23
    
    def __post_init__(self):
        super().__init__(self.master)
        
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.tk_hours = tk.StringVar(value='00')
        self.tk_minutes = tk.StringVar(value='00')
        self.tk_seconds = tk.StringVar(value='00')
        
        self.option_add('*Label*font', ['', 12])
        inner = tk.Frame(self)
        inner.pack(padx=5, pady=5)
        
        self._up = ImageTk.PhotoImage(Image.open("up.png"), (20, 10))
        self._up2 = ImageTk.PhotoImage(Image.open("up2.png"), (20, 10))
        self._down = ImageTk.PhotoImage(Image.open("down.png"), (20, 10))
        self._down2 = ImageTk.PhotoImage(Image.open("down2.png"), (20, 10))
        
        h = tk.Button(inner, image=self._up2, command=lambda: self.on_button('h', 1))
        m = tk.Button(inner, image=self._up2, command=lambda: self.on_button('m', 5))
        s = tk.Button(inner, image=self._up2, command=lambda: self.on_button('s', 5))
        h.grid(row=0, column=0, sticky='we')
        m.grid(row=0, column=2, sticky='we')
        s.grid(row=0, column=4, sticky='we')
        
        m = tk.Button(inner, image=self._up, command=lambda: self.on_button('m', 1))
        s = tk.Button(inner, image=self._up, command=lambda: self.on_button('s', 1))
        m.grid(row=1, column=2, sticky='we')
        s.grid(row=1, column=4, sticky='we')
        
        tk.Label(inner, text='00', textvariable=self.tk_hours).grid(row=2, column=0)
        tk.Label(inner, text=':').grid(row=2, column=1)
        tk.Label(inner, text='00', textvariable=self.tk_minutes).grid(row=2, column=2)
        tk.Label(inner, text=':').grid(row=2, column=3)
        tk.Label(inner, text='00', textvariable=self.tk_seconds).grid(row=2, column=4)
        
        m = tk.Button(inner, image=self._down, command=lambda: self.on_button('m', -1))
        s = tk.Button(inner, image=self._down, command=lambda: self.on_button('s', -1))
        m.grid(row=3, column=2, sticky='we')
        s.grid(row=3, column=4, sticky='we')
        
        h = tk.Button(inner, image=self._down2, command=lambda: self.on_button('h', -1))
        m = tk.Button(inner, image=self._down2, command=lambda: self.on_button('m', -5))
        s = tk.Button(inner, image=self._down2, command=lambda: self.on_button('s', -5))
        h.grid(row=4, column=0, sticky='we')
        m.grid(row=4, column=2, sticky='we')
        s.grid(row=4, column=4, sticky='we')
    
    def on_button(self, unit, amount):
        # amount can be negative
        match unit:
            case 'h':
                self.hours += amount
            case 'm':
                self.minutes += amount
            case 's':
                self.seconds += amount
        
        # validate
        if self.seconds < 0:
            self.seconds = 59
            self.minutes -= 1
        if self.seconds >= 60:
            self.seconds = 0
            self.minutes += 1
        
        if self.minutes < 0:
            self.minutes = 59
            self.hours -= 1
        if self.minutes >= 60:
            self.minutes = 0
            self.hours += 1
        
        if self.hours < 0:
            self.hours = self.hours_limit
        if self.hours >= self.hours_limit + 1:
            self.hours = 0
        
        # update the labels
        self.tk_hours.set(f'{self.hours:02d}')
        self.tk_minutes.set(f'{self.minutes:02d}')
        self.tk_seconds.set(f'{self.seconds:02d}')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TimePicker testing')
    root.geometry('300x300+1000+200')
    root.configure(bg='grey')
    TimePicker(root).pack()
    TimePicker(root, 99).pack()
    root.mainloop()