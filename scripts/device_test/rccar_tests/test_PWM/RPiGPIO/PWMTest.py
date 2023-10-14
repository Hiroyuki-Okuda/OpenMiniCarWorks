# PWM simple output test
#
# Copyright (c) 2023 MODECO
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

import RPi.GPIO as GPIO
import time

print("start PWM initialization...")
GPIO.setmode(GPIO.BCM)

gppin_acc = 12
gppin_str = 13

# Initialize GPIO for PWM
GPIO.setup(gppin_str, GPIO.OUT)
servo_str = GPIO.PWM(gppin_str, 60)
servo_str.start(0)

GPIO.setup(gppin_acc, GPIO.OUT)
servo_acc = GPIO.PWM(gppin_acc, 60)
servo_acc.start(0)

# Prepare neutral position, min&max
# Neutral position would be 9-11% in duty ratio for Tamiya Finespec RC Servo
scale = 0.02319  # Tune here to get range to min/max
neutral = 0.08695  # Tune here to set neutral position  
str_n = neutral
str_m = neutral - scale 
str_M = neutral + scale 

acc_n = neutral
acc_m = neutral - scale 
acc_M = neutral + scale 

servo_str.ChangeDutyCycle( str_n + 0.0*scale)
servo_acc.ChangeDutyCycle( acc_n + 0.0*scale)

print("start control loop")

for i in range(10):
    print("Loop#", i)
    servo_acc.ChangeDutyCycle( acc_n + 0.0*scale)
    servo_str.ChangeDutyCycle( str_n - 0.0*scale)
    time.sleep(1)

print("to end...")
servo_str.ChangeDutyCycle( str_n + 0.0*scale)

time.sleep(5)
servo_str.stop()
servo_acc.stop()

GPIO.cleanup()
print("finish.")
