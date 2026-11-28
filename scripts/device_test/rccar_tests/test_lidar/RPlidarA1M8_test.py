# Lidar test
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
