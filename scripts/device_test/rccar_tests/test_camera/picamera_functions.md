# Picamera2 Basic Functions

This document introduces four basic Picamera2 capabilities: image capture, video recording, camera preview, and camera controls.
For more details, check [Picamera2 Official Manual (PDF)](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)

## 1. Image Capture

Picamera2 provides several ways to capture images.

| Function                          | Description                                                    |
| --------------------------------- | -------------------------------------------------------------- |
| `capture_file()`                  | Capture and save an image to a file                            |
| `capture_array()`                 | Capture an image as a NumPy array                              |
| `capture_image()`                 | Capture an image as a PIL Image                                |
| `switch_mode_and_capture_file()`  | Switch configuration, capture, and save an image               |
| `switch_mode_and_capture_array()` | Switch configuration and return the captured image as an array |

### Example as used in [camera_test.py:26](camera_test.py)

```python
# Save an image
picam2.capture_file("test.jpg")

# Capture as NumPy array
frame = picam2.capture_array()

# Capture as PIL Image
image = picam2.capture_image()

# Switch configuration and capture
picam2.switch_mode_and_capture_file(
    capture_config,
    "test.jpg"
)
```

**Note:** `switch_mode_and_capture_file()` is useful when running a low-resolution video configuration but occasionally needing to capture a high-resolution still image.

## 2. Video Recording

Picamera2 supports continuous video recording using different encoders, such as H.264 and MJPEG.

### Example: H.264 Recording shown in [camera_test_video.py](camera_test_video.py)

### Useful Functions

| Function            | Description                 |
| ------------------- | --------------------------- |
| `start_recording()` | Start video recording       |
| `stop_recording()`  | Stop video recording        |
| `start_encoder()`   | Start an encoder separately |
| `stop_encoder()`    | Stop an encoder separately  |

**Note:** The example saves an H.264 elementary stream. You can convert it into MP4 without re-encoding using FFmpeg:

```bash
ffmpeg -i output.h264 -c:v copy output.mp4
```

## 3. Camera Preview

Picamera2 can display a live camera preview without requiring OpenCV.

It supports different preview backends:

| Preview Backend | Description               |
| --------------- | ------------------------- |
| `Preview.QTGL`  | Qt-based OpenGL preview   |
| `Preview.QT`    | Qt-based software preview |
| `Preview.DRM`   | Direct rendering preview  |

### Example as used in [camera_test.py:8](camera_test.py)

```python
from picamera2 import Picamera2, Preview

picam2 = Picamera2()

# Start preview window
picam2.start_preview(Preview.QTGL)

# Start camera capture
picam2.start()

input("Press Enter to stop...")

picam2.stop_preview()
picam2.stop()
picam2.close()
```

### Useful Functions

| Function          | Description                     |
| ----------------- | ------------------------------- |
| `start_preview()` | Open and display camera preview |
| `stop_preview()`  | Close camera preview            |

**Important:** `picam2.start()` and `picam2.start_preview()` serve different purposes.

- `start()` starts the camera capture pipeline.
- `start_preview()` displays the camera feed in a preview window.

You can capture images and record videos without opening a preview window.

## 4. Camera Controls

Picamera2 allows you to adjust camera settings programmatically.

### Common Camera Controls

| Control        | Description                                  |
| -------------- | -------------------------------------------- |
| `ExposureTime` | Control exposure duration                    |
| `AnalogueGain` | Adjust sensor gain                           |
| `Brightness`   | Adjust image brightness                      |
| `Contrast`     | Adjust image contrast                        |
| `Saturation`   | Adjust color saturation                      |
| `Sharpness`    | Adjust image sharpness                       |
| `AwbEnable`    | Enable/disable automatic white balance       |
| `AeEnable`     | Enable/disable automatic exposure            |
| `FrameRate`    | Control frame rate                           |
| `AfMode`       | Configure autofocus mode (supported cameras) |

### Example: Adjust Camera Settings

```python
picam2.set_controls({
    "ExposureTime": 10000,
    "AnalogueGain": 2.0,
    "Brightness": 0.1,
    "Contrast": 1.2,
    "Saturation": 1.0,
    "AwbEnable": True
})
```

### Example: Continuous Autofocus (IMX708) as shown in [camera_test_picamCV.py](camera_test_picamCV.py)

```python
picam2.set_controls({
    "AfMode": controls.AfModeEnum.Continuous
})
```

### Check Available Camera Controls

Not all cameras support every control. You can check the available controls using:

```python
print(picam2.camera_controls)
```

**Note:** Camera controls should be configured according to the capabilities of the connected camera module.

---

## References

- [Picamera2 Official Manual (PDF)](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [Raspberry Pi Camera Software Documentation](https://www.raspberrypi.com/documentation/accessories/camera-software.html)