# test PRM
import RPi.GPIO as GPIO
import time

print("start PWM initialization...")
GPIO.setmode(GPIO.BCM)

gppin_str = 18

GPIO.setup(gppin_str, GPIO.OUT)
servo_str = GPIO.PWM(gppin_str, 60)
servo_str.start(0)

#
scale = 0.4 / 17.25 
str_n = 0.08695  # 1.5 / 17.25
str_m = str_n - scale # 1.1 / 17.25
str_M = str_n + scale # 1.9 / 17.25

duty = 8.695

servo_str.ChangeDutyCycle( duty)

print("start control loop")

str_n = 0.001
j = -1
for i in range(11):
    print("Loop#", i, j)
    d = duty + j
    print("d", d)
    servo_str.ChangeDutyCycle( d  )
    j = j + 0.2
    time.sleep(1)
    
    
    

print("to end...")
servo_str.ChangeDutyCycle( duty)

#time.sleep(5)
servo_str.stop()

GPIO.cleanup()
print("finish.")
