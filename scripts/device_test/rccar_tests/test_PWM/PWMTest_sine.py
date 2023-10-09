# test PRM
import RPi.GPIO as GPIO
import time
import math

print("start PWM initialization...")
GPIO.setmode(GPIO.BCM)

gppin_str = 13
gppin_acc = 12

GPIO.setup(gppin_str, GPIO.OUT)
servo_str = GPIO.PWM(gppin_str, 60)
servo_str.start(0)

GPIO.setup(gppin_acc, GPIO.OUT)
servo_acc = GPIO.PWM(gppin_acc, 60)
servo_acc.start(0)

#
str_n = 8.4  # 1.5 / 17.25
str_m = str_n - 1 # 1.1 / 17.25
str_M = str_n + 1 # 1.9 / 17.25

acc_n = 9.8
acc_m = acc_n - 1 
acc_M = acc_n + 1

servo_str.ChangeDutyCycle( str_n)
servo_acc.ChangeDutyCycle( acc_n)

print("start control loop")

t = 0
dt = 0.01
N = 1000
for i in range(N):
    s = str_n + 1.5 * math.sin(t*2.0*3.14/4)
    a = acc_n + 2.0 * math.sin(t*2.0*3.14/4)
    #print("Loop#", i, "t", t, "d", d)
    servo_str.ChangeDutyCycle( s  )
    servo_acc.ChangeDutyCycle( a  )
    # shift time
    time.sleep(dt)
    t = t + dt
    
    

print("to end...")
servo_str.ChangeDutyCycle( str_n)

#time.sleep(5)
servo_str.stop()

GPIO.cleanup()
print("finish.")
