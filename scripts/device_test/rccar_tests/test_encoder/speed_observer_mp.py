import multiprocessing
from math import pi
import time

import RPi.GPIO as GPIO

# speed observer program
# copyright 2025 @ MODECO LLC
#
# measure encoder A\B phase with simple logit
# count up/down only A phase changes at rising edge
# [basic logic]
# if A=true & pre-A=false:    # true @ A rises up
#     if B=false:    # phase A advances to phase B
#          count-up
#     else:          # phase B advances to phase A
#          count-down


class SpeedObserver:
    @staticmethod
    def updateSpeed(
        q_speed: multiprocessing.Value,
        q_count: multiprocessing.Value,
        A_PIN,
        B_PIN,
        n_teeth,
        wheel_diameter,
    ):
        """
        Update shared speed (m/s) and count using BCM encoder pins.
        q_speed: shared info for speed (m/s)
        q_count: shared info for count (pulse)
        A_PIN: pin number of encoder A
        B_PIN: pin number of encoder B
        n_teeth: number of teeth on encoder
        wheel_diameter: wheel diameter in meters
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        speed = 0
        last_a_flag = GPIO.input(A_PIN)
        last_fwd_time = 0
        last_bwd_time = 0

        distance_per_tooth = pi * wheel_diameter / n_teeth

        while True:
            a_flag = GPIO.input(A_PIN)
            b_flag = GPIO.input(B_PIN)

            # On an A rising edge, B determines the direction.
            if a_flag and not last_a_flag:
                if not b_flag:
                    # forward
                    q_count.value = q_count.value + 1
                    dt = time.time() - last_fwd_time
                    last_fwd_time = time.time()
                else:
                    # backward
                    q_count.value = q_count.value - 1
                    dt = last_bwd_time - time.time()
                    last_bwd_time = time.time()
                # Distance per tooth divided by time between edges.
                speed = distance_per_tooth / dt
            else:
                # Report zero when no edge has arrived for 0.1 seconds.
                if time.time() - max(last_fwd_time, last_bwd_time) > 0.1:
                    speed = 0

            last_a_flag = a_flag

            q_speed.value = speed


def printQueue(q: multiprocessing.Value, c: multiprocessing.Value):
    DeltaT = 0.1
    while True:
        speed = q.value
        count = c.value
        print(f"{count} : {speed}")
        time.sleep(DeltaT)


def logQueue(q: multiprocessing.Value, c: multiprocessing.Value):
    path = "latest_speedlog.csv"
    DeltaT = 0.01
    cnt = 0
    with open(path, mode="w") as f:
        f.write("step, count, speed\n")
        while True:
            # Record the latest shared values every 10 ms.
            speed = q.value
            count = c.value
            f.write(f"{cnt * DeltaT},{count},{speed}\n")
            time.sleep(DeltaT)
            cnt += 1


def main():
    # BCM pins and wheel dimensions for the ADRC-CAR encoder.
    A_PIN = 22
    B_PIN = 27
    n_teeth = 36
    wheel_diameter = 0.066

    # Share the latest speed and count between processes.
    shared_speed = multiprocessing.Value("d", 0)
    shared_count = multiprocessing.Value("i", 0)

    # create processes
    processes = [
        multiprocessing.Process(
            target=SpeedObserver.updateSpeed,
            args=(
                shared_speed,
                shared_count,
                A_PIN,
                B_PIN,
                n_teeth,
                wheel_diameter,
            ),
        ),
        multiprocessing.Process(target=printQueue, args=(shared_speed, shared_count)),
        multiprocessing.Process(target=logQueue, args=(shared_speed, shared_count)),
    ]

    # start processes
    for process in processes:
        process.start()

    try:
        while True:
            # wait for measurement
            time.sleep(1)
    except KeyboardInterrupt:
        # close processes
        for process in processes:
            process.terminate()
            process.join()
        print("\nclosed all processes")


if __name__ == "__main__":
    main()
