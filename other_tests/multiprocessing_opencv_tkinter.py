"""

https://stackoverflow.com/a/25150139 plus some of my edits
"""

import multiprocessing
from tkinter import *
from tkinter import ttk
import cv2

e = multiprocessing.Event()
p = None

# -------begin capturing and saving video
def startrecording(e):
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    
    size = (frame_width, frame_height) 
    
    # Below VideoWriter object will create 
    # a frame of above defined The output  
    # is stored in 'filename.avi' file. 
    out = cv2.VideoWriter('filename.mp4',  
                            cv2.VideoWriter_fourcc(*'mp4v'), 
                            30, size) 

    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        else:
            break

def start_recording_proc():
    global p
    p = multiprocessing.Process(target=startrecording, args=(e,))
    p.start()

# -------end video capture and stop tk
def stoprecording():
    e.set()
    p.join()

    root.quit()
    root.destroy()

if __name__ == "__main__":
    # -------configure window
    root = Tk()
    root.geometry("%dx%d+0+0" % (100, 100))
    startbutton=ttk.Button(root,text='START',command=start_recording_proc)
    stopbutton=ttk.Button(root,text='STOP', command=stoprecording)
    startbutton.pack()
    stopbutton.pack()

    # -------begin
    root.mainloop()