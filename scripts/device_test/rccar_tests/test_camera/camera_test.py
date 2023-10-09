from picamera2.picamera2 import *
import time

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
#preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
preview_config = picam2.create_preview_configuration(main={"format": 'XBGR8888', "size": (3280, 2464)})
capture_config = picam2.create_still_configuration()

picam2.configure(preview_config)

picam2.start()
time.sleep(5)
picam2.switch_mode_and_capture_file(capture_config, 'test.jpg')