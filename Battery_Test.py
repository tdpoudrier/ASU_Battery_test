"""
Template for main program. Has buttons to start test, end test, and exit program
"""

#Imports
from tkinter import *
from tkinter import ttk

#csv file

#Define root of interface
root = Tk()

#Define frame
frame = ttk.Frame(root, relief='raised')

#Define buttons
button1 = ttk.Button(frame, text='Start Test')
button2 = ttk.Button(frame, text='End Test')
exitButton = ttk.Button(root, text='Exit Program')

#Define label
label = ttk.Label(frame, text='Test not running')

#Bind button actions
button1.bind('<ButtonPress>', lambda e: label.configure(text='Test Running'))
button2.bind('<ButtonPress>', lambda e: label.configure(text='Test not running'))
exitButton.bind('<ButtonPress>', lambda e: root.quit())

#Add elements to frame
frame.grid()
button1.grid()
button2.grid()
label.grid()
exitButton.grid()

#Run mainloop of interface
root.mainloop()