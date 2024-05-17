"""
File: Battery_Test.py
Author: Tevin Poudrier
Date: Tuesday, May 14, 2024 1:22:45 PM
Description: Record ANVIS battery voltage, light level of chamber, and record ANVIS output.
"""

#Imports
from tkinter import *
from tkinter import ttk, font
import csv
from pathlib import Path
import multiprocessing
import cv2
import time
from datetime import datetime
import board
import adafruit_tsl2591
import adafruit_ads1x15.ads1115 as ads
from adafruit_ads1x15.analog_in import AnalogIn

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

    #add header
    append_to_csv(["Voltage", "Lux", "Index"])

#Add data to csv data file
# data must be an iterable
def append_to_csv(data):
    global filename
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data)

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
                            20, size) # TODO - ask ASU about speed of recording

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

#Updates filename, starts recording, and starts test execution.
#Updates information labels
def start_test():
    update_filename()
    start_recording_proc()
    test_timer()

    start_time = datetime.now()

    test_status_label.configure(text='Test Status: Active')
    data_file_label.configure(text='Data file: ' + filename)
    video_file_label.configure(text='Video file: ' + video_file)
    start_time_label.configure(text='Start Time: ' + start_time.strftime("%Y-%m-%d %H:%M:%S"))
    
    start_button.config(state=DISABLED)
    lux_button.config(state=DISABLED)
    
#Record data every second and synchronize count with camera process
#Update information labels
def test_timer():
    global timerID, count
    
    #recursive call every second
    timerID = root.after(1000, test_timer) 
    
    count = count + 1

    #Print elasped time in HH:MM:SS format
    elapsed_time_label.configure(text='Elapsed time: ' + (str( (count // 3600)).zfill(2) ) + ':' 
                                 + (str( (count // 60)).zfill(2) ) + ':' 
                                 + (str( (count % 60)).zfill(2) ) )

    print_lux()

    voltage = AnalogIn(volt_sensor, ads.P0)

    str_volt = "{:.2f}".format(voltage.voltage)

    str_lux = "{:.2f}".format(lux_sensor.lux)

    current_voltage_label.config(text='Current Voltage: ' +  str_volt)
    queue.put(count)
    append_to_csv([float(str_volt), float(str_lux) , count])

    

#stops the test
def stop_test():
    global timerID, count

    if timerID is not None:
        root.after_cancel(timerID)
        timerID = None
        # label.configure(text='Test not running')
        count = 0
        stoprecording()
        start_button.config(state=NORMAL)
        lux_button.config(state=NORMAL)

# Terminate program
def exit_program():
    stop_test()
    root.destroy()

#update lux value displayed
def print_lux():
    lux = "{:.2f}".format(lux_sensor.lux)
    current_lux_label.config(text='Current Lux: ' + str(lux))


if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Initialize the sensor.
    lux_sensor = adafruit_tsl2591.TSL2591(i2c)
    volt_sensor = ads.ADS1115(i2c)

    #Define root of interface
    root = Tk()
    root.defaultFont = font.nametofont("TkDefaultFont") 
    root.defaultFont.configure(family="Segoe UI", 
                                size=28) 
    # root.geometry('300x150')
    root.wm_title("ASU Battery Analyzer")

    #Define frame
    button_frame = ttk.Frame(root, 
                             relief='raised',
                             padding=10,
                             height = 300,
                             width = 300)
    test_info_frame = ttk.Frame(root, 
                                relief='sunken',
                                padding=10,
                                height = 600,
                                width = 100)

    #Define buttons
    start_button = ttk.Button(button_frame, text='Start Test', padding=20)
    stop_button = ttk.Button(button_frame, text='End Test', padding=20)
    exitButton = ttk.Button(button_frame, text='Exit Program', padding=20)
    lux_button = ttk.Button(button_frame, text='Get Lux', padding=20)

    #Define label
    test_status_label = ttk.Label(test_info_frame, text='Test Status: Idle')
    data_file_label = ttk.Label(test_info_frame, text='Data file: ')
    video_file_label = ttk.Label(test_info_frame, text='Video file: ')
    start_time_label = ttk.Label(test_info_frame, text='Start Time: ')
    current_voltage_label = ttk.Label(test_info_frame, text='Current Voltage: ')
    current_lux_label = ttk.Label(test_info_frame, text='Current Lux: ')
    elapsed_time_label = ttk.Label(test_info_frame, text='Elapsed Time: ')

    #Bind button actions
    start_button.configure(command=start_test)
    stop_button.configure(command=stop_test)
    lux_button.configure(command=print_lux)
    exitButton.configure(command=exit_program)
    
    #Add elements to button frame
    start_button.grid(row=0, pady=10)
    stop_button.grid(row=1, pady=10)
    lux_button.grid(row=2, pady=10)
    exitButton.grid(row=3, pady=10)

    #Add elements to test info frame
    test_status_label.grid(sticky='w')
    data_file_label.grid(sticky='w')
    video_file_label.grid(sticky='w')
    start_time_label.grid(sticky='w')
    current_voltage_label.grid(sticky='w')
    current_lux_label.grid(sticky='w')
    elapsed_time_label.grid(sticky='w')

    #Add frames to root
    button_frame.grid(column=0, row=0, sticky='N')
    test_info_frame.grid(column=1, row=0, sticky='N')
    

    #Run mainloop of interface
    root.protocol("WM_DELETE_WINDOW", exit_program)
    root.mainloop()
