import tkinter as tk

from tk_digital_time_picker import TimePicker


root = tk.Tk()
root.title('TimePicker testing')
root.geometry('300x300+1000+200')
root.configure(bg='grey')

TimePicker(root, hours=12, minutes=34, seconds=56).pack()

picker = TimePicker(root, hours_limit=100)
picker.pack()
picker.set_value('99:59:59')

print(picker)
print(picker.get_seconds())

# testing wrapping
picker.seconds += 1
print(picker)

picker.minutes += 60
print(picker)

picker.hours -= 2
print(picker)

root.mainloop()