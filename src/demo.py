import tkinter as tk

from tk_digital_time_picker import TimePicker


root = tk.Tk()
root.title('TimePicker testing')
root.geometry('300x300+1000+200')
root.configure(bg='grey')

TimePicker(root, hours=12, minutes=34, seconds=56).pack()

picker = TimePicker(root, hours_limit=99)
picker.pack()
picker.set_value('66:55:44')

print(picker)
print(picker.get_seconds())

picker.seconds = 100
print(picker.hours, picker.minutes, picker.seconds)

picker.minutes = 100
print(picker.hours, picker.minutes, picker.seconds)

picker.hours = 100
print(picker.hours, picker.minutes, picker.seconds)

root.mainloop()