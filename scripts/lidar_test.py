from rplidar import RPLidar


lidar = RPLidar('/dev/ttyUSB0')
info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)
for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measures' % (i, len(scan)))

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
