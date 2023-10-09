# test PRM
import RPi.GPIO as GPIO
import time

print("start PWM initialization...")
GPIO.setmode(GPIO.BCM)

gppin_str = 18
gppin_acc = 13

GPIO.setup(gppin_str, GPIO.OUT)
servo_str = GPIO.PWM(gppin_str, 60)
servo_str.start(0)

GPIO.setup(gppin_acc, GPIO.OUT)
servo_acc = GPIO.PWM(gppin_acc, 60)
servo_acc.start(0)

#
scale = 0.4 / 17.25 
str_n = 0.08695  # 1.5 / 17.25
str_m = str_n - scale # 1.1 / 17.25
str_M = str_n + scale # 1.9 / 17.25

acc_n = str_n
acc_m = str_m
acc_M = str_M

servo_str.ChangeDutyCycle( str_n + 0.0*scale)
servo_acc.ChangeDutyCycle( acc_n + 0.0*scale)


print("start control loop")

for i in range(10):
    print("Loop#", i)

    servo_str.ChangeDutyCycle( str_n + 0.0*scale)
    time.sleep(1)

    servo_str.ChangeDutyCycle( str_n + 0.0*scale)
    time.sleep(1)

    servo_str.ChangeDutyCycle( str_n + 0.0*scale)
    time.sleep(1)
    
    servo_str.ChangeDutyCycle( str_n - 0.0*scale)
    time.sleep(1)

print("to end...")
servo_str.ChangeDutyCycle( str_n + 0.0*scale)

time.sleep(5)
servo_str.stop()
servo_acc.stop()

GPIO.cleanup()
print("finish.")
