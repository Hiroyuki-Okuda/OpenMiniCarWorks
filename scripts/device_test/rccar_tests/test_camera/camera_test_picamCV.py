import cv2
from picamera2 import Picamera2

# Create a Picamera2 instance
picam2 = Picamera2()

# Configure the camera with a preview mode at 640x480 XRGB8888 format
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))

# Start the camera (no preview window)
picam2.start()

# Set continuous autofocus mode (commented out - enable if needed)
# picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Continuously capture and display frames from the camera
while True:
  # Capture the current frame as a numpy array
  im = picam2.capture_array()

  # Display the frame in a window titled "Camera"
  cv2.imshow("Camera", im)

  # Wait 1ms for a key press (required for OpenCV window to process events)
  key = cv2.waitKey(1)

  # If ESC key (ASCII 27) is pressed, break out of the loop
  if key == 27:
    break

# Stop the camera
picam2.stop()

# Close all OpenCV windows
cv2.destroyAllWindows()