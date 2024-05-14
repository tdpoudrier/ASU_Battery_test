# Python program to save a  
# video using OpenCV 
  
   
import cv2
import time
  
   
# Create an object to read  
# from camera 
video = cv2.VideoCapture(0) 
   
# We need to check if camera 
# is opened previously or not 
if (video.isOpened() == False):  
    print("Error reading video file") 
  
# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
   
size = (frame_width, frame_height) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename.mp4',  
                         cv2.VideoWriter_fourcc(*'mp4v'), 
                         30, size) 

count = 0

color = (0,255,0)
origin = (0,30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(frame):
    #use global count
    global count
    
    #add timestamp to video
    timestamp = time.strftime("%Y-%m-%d %X") + " " + str(count)
    cv2.putText(frame, timestamp, origin, font, scale, color, thickness)

while(True): 
    ret, frame = video.read() 
  
    if ret == True:  
        apply_timestamp(frame)
        # Write the frame into the file
        result.write(frame) 
  
        # Display the frame 
        # saved in the file 
        cv2.imshow('Frame', frame) 
  
        # Press S on keyboard  
        # to stop the process 
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
  
    # Break the loop 
    else: 
        break
  
# When everything done, release  
# the video capture and video  
# write objects 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 