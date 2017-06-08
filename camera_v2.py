from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import time
import cv2
import numpy as np
import requests
import base64
import io
import threading

openface_url = 'http://toosyou.nctu.me:7777'
# openface_url = 'http://localhost:7777'
# openface_url = 'http://192.168.43.35:7777'

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    #Image.open(self.stream)
                    #...
                    #...
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                    header = { 'time': str(time.time()) } # capture time
                    # image = cv2.imencode('.jpg', numpy.fromstring(self.stream.getvalue(), dtype=numpy.uint8) )[1].tostring()
                    try:
                        requests.post(openface_url, data=str(self.stream.getvalue()), headers=header)
                        print('Sent!')
                        # time.sleep(5)
                    except:
                        print('Unsent!')
                        time.sleep(4)

                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]
    camera.resolution = (240, 240)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), format='jpeg', use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
