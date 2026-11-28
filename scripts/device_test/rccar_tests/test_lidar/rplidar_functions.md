# RPLidar Basic Functions

This document introduces the basic functions of the Python `rplidar` library for connecting to the sensor, checking its status, and reading measurements. For installation and hardware setup, see the [LiDAR setup guide](README.md).

## 1. Connection and Device Status

| Function | Description |
| -------- | ----------- |
| `RPLidar(port)` | Initialize the LiDAR connection using a serial port |
| `get_info()` | Retrieve device information |
| `get_health()` | Check device health |
| `disconnect()` | Close the serial connection |

### Device status as used in [RPlidarA1M8_test.py](RPlidarA1M8_test.py)

```python
print('Device info:', lidar.get_info())
print('Health:', lidar.get_health())
```

**Note:** Replace `/dev/ttyUSB0` with the serial port assigned to your LiDAR.

## 2. Reading Measurements and Scans

| Function | Description |
| -------- | ----------- |
| `iter_measures()` | Retrieve individual measurements |
| `iter_scans()` | Retrieve complete scans |

`iter_measures()` yields tuples of `(new_scan, quality, angle, distance)`. The `new_scan` flag marks the beginning of a scan. `iter_scans()` groups measurements into scans, each containing `(quality, angle, distance)` tuples. Angles are in degrees and distances are in millimeters.

### Example: Read individual measurements

```python
for new_scan, quality, angle, distance in lidar.iter_measures():
    print(new_scan, quality, angle, distance)
```

### Reading scans as used in [RPlidarA1M8_test.py](RPlidarA1M8_test.py)

```python
for i, scan in enumerate(lidar.iter_scans()):
    print(f'Scan {i}: {len(scan)} measurements')
    print(scan[:5])
    if i >= 9:
        break
```

See [test_obstacle_detection.py](test_obstacle_detection.py) for an example that filters scans for nearby obstacles, and [animate.py](animate.py) for a live polar-plot visualization.

## 3. Motor Control and Cleanup

| Function | Description |
| -------- | ----------- |
| `start_motor()` | Start the LiDAR motor |
| `stop_motor()` | Stop the LiDAR motor |
| `stop()` | Stop scanning |
| `disconnect()` | Close the serial connection |

### Example: Check status, scan, and clean up

The combined [RPlidarA1M8_test.py](RPlidarA1M8_test.py) reads 10 scans, or stops earlier if interrupted with `Ctrl+C`:

```python
from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')

try:
    print('Device info:', lidar.get_info())
    print('Health:', lidar.get_health())

    for i, scan in enumerate(lidar.iter_scans()):
        print(f'Scan {i}: {len(scan)} measurements')
        print(scan[:5])
        if i >= 9:
            break
except KeyboardInterrupt:
    pass
finally:
    try:
        lidar.stop()
    finally:
        try:
            lidar.stop_motor()
        finally:
            lidar.disconnect()
```

Use `start_motor()` when you need to explicitly start the motor, and stop scanning and the motor before disconnecting after a scan.

---

## References

- [RPLidar Python library and examples](https://github.com/Roboticia/RPLidar)
- [Raspberry Pi LiDAR setup and testing](README.md)
