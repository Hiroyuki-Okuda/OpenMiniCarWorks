from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Create a Picamera2 instance for camera access
picam2 = Picamera2()

# Create a video configuration at 1280x720 resolution
video_config = picam2.create_video_configuration(main={"size": (1280, 720)})

# Apply the video configuration to the camera
picam2.configure(video_config)

# Create an H264 encoder with a bitrate of 10 Mbps
encoder = H264Encoder(bitrate=10_000_000)

# Start recording H264 video using the encoder, saving to "output.h264"
picam2.start_recording(encoder, "output.h264")

try:
    print("Recording... Press Ctrl+C to stop.")
    # Keep the script running to maintain the recording loop
    while True:
        pass

except KeyboardInterrupt:
    # Stop recording when Ctrl+C is pressed
    print("Recording stopped.")

finally:
    # Stop the camera recording and close the Picamera2 instance
    picam2.stop_recording()
    picam2.close()
