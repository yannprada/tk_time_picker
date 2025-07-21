# TimePicker

tkinter widget.

Button that displays time in `HH:MM:SS` format. When clicked, opens a window to edit time.

Methods:
```python
TimePicker.__str__()				# -> str: format 'HH:MM:SS'
TimePicker.get_seconds()			# -> int: total seconds
TimePicker.set_value(value: str)	# value format: 'HH:MM:SS'
```

## Demo

```python
import tkinter as tk

root = tk.Tk()
root.title('TimePicker testing')
root.geometry('300x300+1000+200')
root.configure(bg='grey')
TimePicker(root).pack()
TimePicker(root, hours_limit=99).pack()
root.mainloop()
```

![TimePicker test](test.png "TimePicker test")
