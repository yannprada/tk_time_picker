```python
root = tk.Tk()
root.title('TimePicker testing')
root.geometry('300x300+1000+200')
root.configure(bg='grey')
TimePicker(root).pack()
TimePicker(root, 99).pack()
root.mainloop()
```

![TimePicker test](test.png "TimePicker test")
