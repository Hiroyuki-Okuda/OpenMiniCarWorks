from picamera2.picamera2 import *
import time

# Create a Picamera2 instance
picam2 = Picamera2()

# Start a QTGL preview window
picam2.start_preview(Preview.QTGL)

# Create a preview configuration at 3280x2464 resolution with XBGR8888 format (4 bit per pixel)
preview_config = picam2.create_preview_configuration(main={"format": 'XBGR8888', "size": (3280, 2464)})

# Create a still image configuration
capture_config = picam2.create_still_configuration()

# Apply the preview configuration to the camera
picam2.configure(preview_config)

# Start the camera preview
picam2.start()

# Wait 5 seconds for camera warmup and stabilization
time.sleep(5)

# Switch to still mode and capture a photo, saving as 'test.jpg'
picam2.switch_mode_and_capture_file(capture_config, 'test.jpg')