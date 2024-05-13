"""
Read data from csv file and display matplotlib graph on tkinter

"""

import tkinter

import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

import csv

data = np.array([])

#Get data from csv file
with open('data.txt', 'r', newline='') as read_file, open('data.csv', 'w', newline='') as write_file:
    reader = csv.reader(read_file, delimiter=',')
    writer = csv.writer(write_file)
    for row in reader:
        data = np.append(data, row)

#Create Tk window
root = tkinter.Tk()
root.wm_title("Embedding in Tk")

#Create matplotlib graph
fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, len(data), 1)
ax = fig.add_subplot()
line, = ax.plot(t, data)
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")

#Add figure to tk drawing area
frame = tkinter.Frame(root, relief='raised')
canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
canvas.draw()

#Quit button
button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

#Place widgets on Tk window
frame.pack()
button_quit.pack(side=tkinter.BOTTOM)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

#Define hid graph button
button_hide_graph = tkinter.Button(master=root, text="Hide Plot")
button_hide_graph.bind('<ButtonPress>', lambda e: canvas.get_tk_widget().pack_forget())
button_hide_graph.pack()

#Define show graph button
button_show_graph = tkinter.Button(master=root, text="Show Plot")
button_show_graph.bind('<ButtonPress>', lambda e: canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True))
button_show_graph.pack()

tkinter.mainloop()
