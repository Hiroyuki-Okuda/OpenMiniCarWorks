import multiprocessing
import RPi.GPIO as GPIO
from math import pi
import time


class SpeedObserver(object):
    @staticmethod
    def updateSpeed(
            q_speed: multiprocessing.Queue,
            A_PIN: int = 22,
            B_PIN: int = 27,
            n_teeth: int = 36,
            wheel_diameter: float = 0.06
        ):
        '''
        Add speed to queue from encoder.

        q_speed: queue of speed (m/s)
        A_PIN: pin number of encoder A
        B_PIN: pin number of encoder B
        n_teeth: number of teeth on encoder
        wheel_diameter: wheel diameter in meters
        '''
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # initialize variables
        speed = 0
        last_a_flag = 0
        last_fwd_time = 0
        last_bwd_time = 0

        while True:
            a_flag = GPIO.input(A_PIN)
            b_flag = GPIO.input(B_PIN)

            if a_flag and not last_a_flag:
                if not b_flag:
                    # forward
                    dt = time.time() - last_fwd_time
                    last_fwd_time = time.time()
                else:
                    # backward
                    dt = last_bwd_time - time.time()
                    last_bwd_time = time.time()
                # update speed
                speed = (pi * wheel_diameter / n_teeth) / dt

            last_a_flag = a_flag

            # remove queue if full
            if q_speed.full():
                q_speed.get()

            # add speed to queue
            q_speed.put(speed)


def printQueue(q: multiprocessing.Queue):
    while True:
        print(q.get())
        time.sleep(0.1)


def main():
    # parameters
    A_PIN = 22
    B_PIN = 27
    n_teeth = 36
    wheel_diameter = 0.06

    # create queues
    q_speed = multiprocessing.Queue(2)

    # create processes
    processes = [
        multiprocessing.Process(
            target=SpeedObserver.updateSpeed,
            args=(q_speed, A_PIN, B_PIN, n_teeth, wheel_diameter,)
        ),
        multiprocessing.Process(
            target=printQueue,
            args=(q_speed,)
        )
    ]

    # start processes
    for process in processes:
        process.start()

    try:
        while True:
            time.sleep(1e5)
    except KeyboardInterrupt:
        # close processes
        for process in processes:
            process.terminate()
            process.join()
        print("\nclosed all processes")


if __name__ == "__main__":
    main()
