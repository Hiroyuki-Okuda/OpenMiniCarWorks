import time
import utilities
import RPi.GPIO as GPIO

# initialize
print("PWM Jog control...")

#PWM_Hz = 60 
#PWM_NeutralSpd = 8.695  #@60Hz
#PWM_NeutralStr = 8.695  #@60Hz

PWM_Hz = 70 
PWM_NeutralStr = 9.65  #@70Hz
PWM_NeutralSpd = 10.08

Delta_Jog = 0.02

spd_ref = PWM_NeutralSpd
str_ref = PWM_NeutralStr

GPIO.setmode(GPIO.BCM)

gppin_str = 13
gppin_acc = 12

GPIO.setup(gppin_str, GPIO.OUT)
servo_str = GPIO.PWM(gppin_str, PWM_Hz)
servo_str.start(0)

GPIO.setup(gppin_acc, GPIO.OUT)
servo_acc = GPIO.PWM(gppin_acc, PWM_Hz)
servo_acc.start(0)

servo_str.ChangeDutyCycle( PWM_NeutralStr )
servo_acc.ChangeDutyCycle( PWM_NeutralSpd )
time.sleep(1)

def write_help():
    print("Enter: stop, w&d:speed, a&d:steering")

write_help()

try:                        # try:の部分にループ処理を書く
    i = 0
    while True:
        # loop count
        i = i + 1
        
        # key polling
        key = utilities.getkey()
        if key == 10:
            break
        if key == ord('w'):
            spd_ref = spd_ref + Delta_Jog
        if key == ord('s'):
            spd_ref = spd_ref - Delta_Jog
        if key == ord('a'):
            str_ref = str_ref - Delta_Jog
        if key == ord('d'):
            str_ref = str_ref + Delta_Jog
        if key == ord('n'):
            str_ref = PWM_NeutralStr
            spd_ref = PWM_NeutralSpd
        servo_str.ChangeDutyCycle( str_ref )
        servo_acc.ChangeDutyCycle( spd_ref )
        
        # info disp
        if i % 20 == 0:
            print("str,spd=",'{:.4g}'.format(str_ref), '{:.4g}'.format(spd_ref))
        if i % 200 == 0:
            write_help()
            
        # wait        
        time.sleep(0.01)
        
        
except KeyboardInterrupt:   # exceptに例外処理を書く
    print('stop!')
    servo_str.stop()
    servo_acc.stop()
    GPIO.cleanup()

servo_str.stop()
servo_acc.stop()
GPIO.cleanup()
print("finish.")

