from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')

try:
    print("Device info:", lidar.get_info())
    print("Health:", lidar.get_health())

finally:
    lidar.disconnect()