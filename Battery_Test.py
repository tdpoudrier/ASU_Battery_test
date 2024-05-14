"""
File: Battery_Test.py
Author: Tevin Poudrier
Date: Tuesday, May 14, 2024 1:22:45 PM
Description: Record ANVIS battery voltage, light level of chamber, and record ANVIS output.
"""

#Imports
from tkinter import *
from tkinter import ttk
import csv
from pathlib import Path
import multiprocessing
import cv2
import time

#Global variables (variables that are modified in functions)
timerID = None
count = 0
filename = "ASU_Battery_test_0.csv"
video_file = "ASU_Battery_test_0.mp4"
test_started = False

#multiprocessing variables
multi_event = multiprocessing.Event()
multi_process = None

#Update filename and video_file to have a unique name to avoid overwritting previous test data
def update_filename():
    global filename, video_file
    file_count = 0
    my_file = Path(filename)
    
    #increment file count if file already exists and update names
    while my_file.is_file():
        
        index1 = filename.rfind('_')
        index2 = filename.rfind('.')
        
        filename = filename[:index1 + 1] + str(file_count) + filename[index2:]
        video_file = filename[:index1 + 1] + str(file_count) + ".mp4"
        
        my_file = Path(filename)
        file_count = file_count + 1
    
    #create a new csv file
    open(filename, 'x', newline = '')

#Add data to csv data file
def append_to_csv(data):
    global filename
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([data])

#Start and record video capture on seperate process
def startrecording(e, queue, video_file):
    
    #Initialize video capture
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    size = (frame_width, frame_height) 
    
    # Create video recorder and encoding
    out = cv2.VideoWriter(video_file,  
                            cv2.VideoWriter_fourcc(*'mp4v'), 
                            30, size) 

    # Record video
    while(cap.isOpened()):
        #stop recording when parent process sets this process
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        
        ret, frame = cap.read()
        if ret==True:
            #Get count value from main process
            if (not queue.empty()):
                count = queue.get()
            
            #Add timestamp to video
            timestamp = time.strftime("%Y-%m-%d %X") + " " + str(count)
            cv2.putText(frame, 
                        timestamp, 
                        (0,30),                     #origin
                        cv2.FONT_HERSHEY_SIMPLEX,   #font 
                        1,                          #scale 
                        (0,255,0),                  #color
                        2)                          #thickness
            out.write(frame)
        else:
            break

#Start the recording on a new process
def start_recording_proc():
    global multi_process
    multi_process = multiprocessing.Process(target=startrecording, args=(multi_event,queue, video_file))
    multi_process.start()

# end video capture
def stoprecording():
    multi_event.set()
    multi_process.join()

#Start the test, this method uses recursion to save data every second
def start_test():
    global timerID, count, label, test_started
    
    timerID = root.after(1000, start_test) 
    string = "Test Running " + str(count)
    count = count + 1
    label.configure(text=string)
    queue.put(count)
    
    if (not test_started):
        update_filename()
        test_started = True
        start_recording_proc()
    
    append_to_csv(count)

#stops the test
def stop_test():
    global timerID, count, test_started

    if timerID is not None:
        root.after_cancel(timerID)
        timerID = None
        label.configure(text='Test not running')
        count = 0
        test_started = False
        stoprecording()

# Terminate program
def exit_program():
    stop_test()
    root.destroy()

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    #Define root of interface
    root = Tk()
    root.geometry('300x150')

    #Define frame
    frame = ttk.Frame(root, relief='raised')

    #Define buttons
    button1 = ttk.Button(frame, text='Start Test')
    button2 = ttk.Button(frame, text='End Test')
    exitButton = ttk.Button(root, text='Exit Program')

    #Define label
    label = ttk.Label(frame, text='Test not running')
    
    #Bind button actions
    button1.configure(command=start_test)
    button2.configure(command=stop_test)
    exitButton.configure(command=exit_program)

    #Add elements to frame
    frame.grid()
    button1.grid()
    button2.grid()
    label.grid()
    exitButton.grid()

    #Run mainloop of interface
    root.mainloop()