# Jog operation with keyboard 
#
# Copyright (c) 2023 MODECO
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

# [NOTE]
# (need to start pigpio daemon before running this script, )
# sudo pigpiod
# 
# (to install pigpio, )
# sudo apt-get install pigpio

import time
import utilities
import pigpio

# in pigpio, 1000,000 = 100% 
# then duty100(100) = 100% duty rate
def duty100(rate):
    # min and max for safety input
    PWM_SAFE_MIN = 7.50 
    PWM_SAFE_MAX = 13.00 
    if rate > PWM_SAFE_MAX:
        rate = PWM_SAFE_MAX
    if rate < PWM_SAFE_MIN:
        rate = PWM_SAFE_MIN
    return int(rate * 10000)

# initialize
print("PWM Jog control...")

# calibration parameters 

Delta_Jog = 0.05 # jog stepping

#PWM_Hz = 60 
#PWM_NeutralSpd = 8.695  #@60Hz 
#PWM_NeutralStr = 8.695  #@60Hz

PWM_Hz = 70 
PWM_NeutralStr = 10.00  #@70Hz
PWM_NeutralSpd = 10.48 #@70Hz
PWM_CruiseSpd = 10.48 - 1.4 #@70Hz # Cruising speed 

spd_ref = PWM_NeutralSpd
str_ref = PWM_NeutralStr

# PWM ioutput pins (hardware PWM works only with 12/13(or 18/19) in RPi)
gppin_acc = 12
gppin_str = 13

# start hardware PWM
pi = pigpio.pi()
pi.set_mode(gppin_acc, pigpio.OUTPUT)
pi.set_mode(gppin_str, pigpio.OUTPUT)


# GPIO12: Hz, duty ratio
pi.hardware_PWM(gppin_acc, PWM_Hz, duty100(10.5))
# GPIO13: Hz, duty ratio
pi.hardware_PWM(gppin_str, PWM_Hz, duty100(10.5))
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
            spd_ref = spd_ref - Delta_Jog 
        if key == ord('s'):
            spd_ref = spd_ref + Delta_Jog 
        if key == ord('a'):
            str_ref = str_ref - Delta_Jog 
        if key == ord('d'):
            str_ref = str_ref + Delta_Jog
        if key == ord('n'):
            str_ref = PWM_NeutralStr
            spd_ref = PWM_NeutralSpd
        # GPIO12: Hz、duty比0.5
        pi.hardware_PWM(gppin_acc, PWM_Hz, duty100(spd_ref))
        # GPIO13: Hz、duty比0.1
        pi.hardware_PWM(gppin_str, PWM_Hz, duty100(str_ref))
        
        # info disp
        if i % 20 == 0:
            print("str,spd=",'{:.4g}'.format(str_ref), '{:.4g}'.format(spd_ref))
        if i % 200 == 0:
            write_help()
            
        # wait        
        time.sleep(0.01)
        
        
except KeyboardInterrupt:   # exceptに例外処理を書く
    print('stop!')
    # GPIO12: Hz、duty比0.5
    pi.hardware_PWM(gppin_acc, PWM_Hz, duty100(PWM_NeutralSpd))
    # GPIO13: Hz、duty比0.1
    pi.hardware_PWM(gppin_str, PWM_Hz, duty100(PWM_NeutralStr))
    #pi.stop()

# GPIO12: Hz、duty比0.5
pi.hardware_PWM(gppin_acc, PWM_Hz, duty100(PWM_NeutralSpd))
# GPIO13: Hz、duty比0.1
pi.hardware_PWM(gppin_str, PWM_Hz, duty100(PWM_NeutralStr))
#pi.stop()
print("finish.")

