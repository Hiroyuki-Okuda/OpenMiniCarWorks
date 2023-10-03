import time
import pigpio


# throttle & steer gpio pin
STEER_PIN = 17
THROTTLE_PIN = 18
NEUTERAL_INPUT = 1500

pi = pigpio.pi()

accel = 50
steer = 200
    

def neuteral():
    pi.set_servo_pulsewidth(STEER_PIN,NEUTERAL_INPUT)
    pi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT)


def circle():
    print("circle")
    try:
        while True:
            pi.set_servo_pulsewidth(STEER_PIN,NEUTERAL_INPUT+steer)
            pi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT-accel)
    except KeyboardInterrupt:
        neuteral()


def stopandgo():
    print("stop & go")
    count = 0
    wait_time = 1
    try:
        for i in range(3):
            print(count)
            pi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT-accel)
            time.sleep(wait_time)
            pi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT)
            time.sleep(wait_time)
            count += 1
        neuteral()
    except KeyboardInterrupt:
        neuteral()


def zigzag():
    zigzag
    print("zigzag")
    count = 0
    wait_time = 1
    try:
        for i in range(3):
            print(count)
            pi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT-accel)
            pi.set_servo_pulsewidth(STEER_PIN,NEUTERAL_INPUT+steer)
            time.sleep(wait_time)
            pi.set_servo_pulsewidth(STEER_PIN,NEUTERAL_INPUT-steer)
            time.sleep(wait_time)
            count += 1
        neuteral()
    except KeyboardInterrupt:
        neuteral()


def run():
    neuteral()
    # circle()
    # stopandgo()
    # zigzag()


if __name__ == "__main__":
    run()
