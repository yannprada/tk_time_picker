import tkinter as tk
from dataclasses import dataclass
from PIL import Image
from PIL.ImageTk import PhotoImage
import pathlib


script_location = pathlib.Path(__file__).parent
images_names = ['up2.png', 'up.png', 'down2.png', 'down.png']
images_paths = list(map(lambda n: f'{script_location}/{n}', images_names))


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
    
    def set_value(self, value):
        value = value.split(':')
        self._hours.set_value(value[0])
        self._minutes.set_value(value[1])
        self._seconds.set_value(value[2])


@dataclass
class UnitPicker(tk.Frame):
    master: tk.Widget
    maxi: int = 59
    increment: int = 1
    increment2: int = 5
    value: int = 0
    
    def __post_init__(self):
        super().__init__(self.master)
        
        self.tk_value = tk.StringVar(value='00')
        
        top = tk.Frame(self)
        bottom = tk.Frame(self)
        label = tk.Label(self, textvariable=self.tk_value, font=['', 12])
        
        top.pack()
        label.pack()
        bottom.pack()
        
        self.buttons = []
        self._add_button(images_paths[0], self.increment2, top)
        self._add_button(images_paths[1], self.increment, top, 1)
        self._add_button(images_paths[2], -self.increment2, bottom)
        self._add_button(images_paths[3], -self.increment, bottom, 1)
        
        for widget in [self, top, bottom, label]:
            widget.bind('<Enter>', self.show_buttons)
            widget.bind('<FocusIn>', self.show_buttons)
            widget.bind('<Leave>', self.hide_buttons)
            widget.bind('<FocusOut>', self.hide_buttons)
    
    def show_buttons(self, event):
        for button in self.buttons:
            button.grid()
    
    def hide_buttons(self, event):
        for button in self.buttons:
            button.grid_remove()
    
    def _add_button(self, image_path, increment, parent, column=0):
        image = PhotoImage(Image.open(image_path))
        button = tk.Button(parent, image=image, command=lambda: self.add(increment))
        # keep a reference to prevent PIL from garbage collecting the image
        button._ref_image = image
        button.grid(row=0, column=column)
        button.after(100, button.grid_remove)
        self.buttons.append(button)
    
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
        
        self._update()
    
    def _update(self):
        self.tk_value.set(f'{self.value:02d}')
    
    def __str__(self):
        return self.tk_value.get()
    
    def set_value(self, value):
        self.value = int(value)
        self._update()


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