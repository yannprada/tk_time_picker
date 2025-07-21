# TimePicker

tkinter widget.

Button that displays time in `HH:MM:SS` format. When clicked, opens a window to edit time.

## Install

```console
pip install tk_digital_time_picker
```

Methods:
```python
TimePicker.__str__()				# -> str: format 'HH:MM:SS'
TimePicker.get_seconds()			# -> int: total seconds
TimePicker.set_value(value: str)	# value format: 'HH:MM:SS'
```

## Demo

```python
import tkinter as tk
from tk_digital_time_picker.time_picker import TimePicker

root = tk.Tk()
root.title('TimePicker testing')
root.geometry('300x300+1000+200')
root.configure(bg='grey')
TimePicker(root).pack()
TimePicker(root, hours_limit=99).pack()
root.mainloop()
```

![TimePicker test](https://github.com/yannprada/tk_time_picker/blob/987f5785e7991f41b44a87a61cbf15af99572c24/test.png "TimePicker test")
