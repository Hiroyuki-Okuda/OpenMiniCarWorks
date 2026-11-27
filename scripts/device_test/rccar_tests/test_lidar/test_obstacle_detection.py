
from rplidar import RPLidar

PORT = '/dev/ttyUSB0'

# Obstacle detection parameters
DETECTION_ANGLE = 30       # degrees (left/right)
DETECTION_DISTANCE = 500   # mm


def detect_obstacle(scan):
    """
    Detect obstacles within the front detection area.

    Args:
        scan: List of (quality, angle, distance) measurements.

    Returns:
        Closest obstacle distance in mm, or None if not detected.
    """
    obstacles = []

    for quality, angle, distance in scan:

        # Ignore invalid measurements
        if quality == 0 or distance <= 0:
            continue

        # Check if the measurement is in front of the vehicle
        is_in_front = (
            angle <= DETECTION_ANGLE
            or angle >= 360 - DETECTION_ANGLE
        )

        # Check if the obstacle is within the detection distance
        if is_in_front and distance <= DETECTION_DISTANCE:
            obstacles.append(distance)

    if obstacles:
        return min(obstacles)

    return None


def main():
    lidar = RPLidar(PORT)

    try:
        print("Starting obstacle detection...")

        for scan in lidar.iter_scans():
            distance = detect_obstacle(scan)

            if distance is not None:
                print(f"Obstacle detected: {distance:.1f} mm")
            else:
                print("No obstacle detected")

    except KeyboardInterrupt:
        print("\nStopping obstacle detection...")

    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()


if __name__ == "__main__":
    main()
