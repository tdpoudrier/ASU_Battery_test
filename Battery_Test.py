"""
Has buttons to start test, end test, and exit program
The test is a second counter that is displayed on interface

counter uses a recursive method that calls root.after(1000, method)
"""

#Imports
from tkinter import *
from tkinter import ttk
import csv
from pathlib import Path

#Global variables
timerID = None
count = 0
filename = "ASU_Battery_test_0.csv"
file_created = False

#Create new file name
def update_filename():
    global filename
    file_count = 0
    my_file = Path(filename)
    while my_file.is_file():
        # file exists
        index1 = filename.rfind('_')
        index2 = filename.rfind('.')
        filename = filename[:index1 + 1] + str(file_count) + filename[index2:]
        my_file = Path(filename)
        file_count = file_count + 1
    open(filename, 'x', newline = '')

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

def append_to_csv(data):
    global filename
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([data])

#start the timer, call using button.configure(command=start_timer)
def start_test():
    global timerID, count, label, file_created
    
    timerID = root.after(1000, start_test) 
    string = "Test Running " + str(count)
    count = count + 1
    label.configure(text=string)
    
    if (not file_created):
        update_filename()
        file_created = True
    
    append_to_csv(count)

#stops the timer, call using button.configure(command=start_timer)
def stop_test():
    global timerID, count, file_created

    if timerID is not None:
        root.after_cancel(timerID)
        timerID = None
        label.configure(text='Test not running')
        count = 0
        file_created = False

#Bind button actions
button1.configure(command=start_test)
button2.configure(command=stop_test)
exitButton.bind('<ButtonPress>', lambda e: root.quit())

#Add elements to frame
frame.grid()
button1.grid()
button2.grid()
label.grid()
exitButton.grid()

#Run mainloop of interface
root.mainloop()