from picamera2 import Picamera2, Preview, MappedArray
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
import time
import cv2
from libcamera import Transform

# init and configure picamera2
picam2 = Picamera2()
camera_config = picam2.create_video_configuration()

#define output file
encoder = H264Encoder()
output = FfmpegOutput('test.mp4')

picam2.configure(camera_config)

#Text parameters for timestamp
color = (0,255,0)
origin = (0,30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

count = 0

def apply_timestamp(request):
    #use global count
    global count
    
    #add timestamp to video
    timestamp = time.strftime("%Y-%m-%d %X") + " " + str(count)
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, color, thickness)
    

#Call apply_timestamp before callback so text is visable
picam2.pre_callback = apply_timestamp

#Display preview and record
picam2.start_preview(Preview.QTGL, x=-10, y=0, width=500, height=400)
transform = Transform(vflip=1)
picam2.start_recording(encoder, output, quality=Quality.MEDIUM)

#Record for 10,000 seconds
while(count < 10000):
    count = count + 1
    time.sleep(1)

#stop preview and recording
picam2.stop_recording()
picam2.stop_preview()