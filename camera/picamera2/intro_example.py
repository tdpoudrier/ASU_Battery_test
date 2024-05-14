"""
Show picamera2 preview and take picture after 2 seconds
"""

from picamera2 import Picamera2, Preview
import time

#initalize and start picamera 2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

#take picture after 2 seconds
time.sleep(2)
picam2.capture_file("test.jpg")