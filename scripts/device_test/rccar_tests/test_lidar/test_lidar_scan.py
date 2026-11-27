from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')

try:
    for i, scan in enumerate(lidar.iter_scans()):
        print(f"Scan {i}: {len(scan)} measurements")
        print(scan[:5])

except KeyboardInterrupt:
    pass

finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()  