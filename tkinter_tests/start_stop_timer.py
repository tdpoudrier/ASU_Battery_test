"""
Has buttons to start test, end test, and exit program
The test is a second counter that is displayed on interface

counter uses a recursive method that calls root.after(1000, method)
"""

#Imports
from tkinter import *
from tkinter import ttk

timerID = None
count = 0

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


#start the timer, call using button.configure(command=start_timer)
def start_timer():
    global timerID
    timerID = root.after(1000, start_timer)
    global count
    global label
    string = "Test Running " + str(count)
    count = count + 1
    label.configure(text=string)

#stops the timer, call using button.configure(command=start_timer)
def stop_timer():
    global timerID
    global count
    if timerID is not None:
        root.after_cancel(timerID)
        timerID = None
        label.configure(text='Test not running')
        count = 0

#Bind button actions
button1.configure(command=start_timer)
button2.configure(command=stop_timer)
exitButton.bind('<ButtonPress>', lambda e: root.quit())

#Add elements to frame
frame.grid()
button1.grid()
button2.grid()
label.grid()
exitButton.grid()

#Run mainloop of interface
root.mainloop()