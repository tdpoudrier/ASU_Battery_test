"""
Create a simple interface with a hello world label and a exit button.
Uses a recursive timer to update and print the seconds the program has run
"""

from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)
label = ttk.Label(frm, text="Hello World!")
button = ttk.Button(frm, text="Quit", command=root.destroy)

count = 0

def recursive_timer():
    root.after(1000, recursive_timer)
    global count
    global label
    string = "Hello World: " + str(count)
    count = count + 1
    label.configure(text=string)


#add elements to frame
frm.grid()
label.grid(column=0, row=0)
button.grid(column=0, row=1)

#start timer
recursive_timer()

#start tkinter
root.mainloop()
