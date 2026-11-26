"""Display the two encoder input states."""

import time

import RPi.GPIO as GPIO


def main():
    # BCM GPIO numbers, not physical header pin numbers.
    A_PIN = 22
    B_PIN = 27

    print("initialize...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            # Sample both channels every 10 ms.
            print(f"A:{GPIO.input(A_PIN)} B:{GPIO.input(B_PIN)}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nterminated.")
    finally:
        GPIO.cleanup((A_PIN, B_PIN))


if __name__ == "__main__":
    main()
