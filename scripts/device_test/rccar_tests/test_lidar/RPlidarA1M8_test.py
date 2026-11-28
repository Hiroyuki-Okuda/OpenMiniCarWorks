# Lidar test
from rplidar import RPLidar


# Change the port if the LiDAR is assigned a different device.
lidar = RPLidar('/dev/ttyUSB0')

try:
    # Check the device information and health before scanning.
    print('Device info:', lidar.get_info())
    print('Health:', lidar.get_health())

    # Show the first five measurements from each of 10 scans.
    for i, scan in enumerate(lidar.iter_scans()):
        print(f'Scan {i}: {len(scan)} measurements')
        print(scan[:5])
        if i >= 9:
            break
except KeyboardInterrupt:
    pass
finally:
    # Stop scanning and the motor, then close the connection.
    try:
        lidar.stop()
    finally:
        try:
            lidar.stop_motor()
        finally:
            lidar.disconnect()
