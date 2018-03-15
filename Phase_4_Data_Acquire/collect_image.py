from time import sleep
from picamera import PiCamera

FRAME_WIDTH = 160
FRAME_HEIGHT = 120
FRAME_FPS = 10

camera = PiCamera()
camera.resolution = (FRAME_WIDTH, FRAME_HEIGHT)
camera.framerate = FRAME_FPS
# camera.start_preview()
print("Camera preheating...")
sleep(3)

for filename in camera.capture_continuous('/home/pi/img/{counter:06d}.jpg', use_video_port=True):
    print('Captured %s' % filename)

