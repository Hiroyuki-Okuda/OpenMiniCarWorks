# PWM simple output test
#
# Copyright (c) 2023 MODECO
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

import pigpio
import time
from TamiyaRcPwm import TamiyaRcPwm

print("start PWM initialization...")

rccar = TamiyaRcPwm()

rccar.PWM_SPD_NEUTRAL = 9.65
PWM_NeutralStr = 9.65  # % in duty ratio @70Hz
PWM_NeutralSpd = 10.48 # % in duty ratio @70Hz

# start hardware PWM
pi = pigpio.pi()
pi.set_mode(gppin_acc, pigpio.OUTPUT)
pi.set_mode(gppin_str, pigpio.OUTPUT)

# Set PWM duty ratio. 1000,000 (1M) = 100% 
# Speed control : GPIO12: Hz, duty ratio
pi.hardware_PWM(gppin_acc, PWM_Hz, int(PWM_NeutralSpd / 100.0 * 1000000) )
# Steering control : GPIO13: Hz, duty ratio
pi.hardware_PWM(gppin_str, PWM_Hz, int(PWM_NeutralStr / 100.0 * 1000000) )
time.sleep(1)

print("Start control loop")

for i in range(10):
    print("Loop#", i)
    Ref_Spd = PWM_NeutralSpd
    Ref_Str = PWM_NeutralStr
    # Speed control : GPIO12: Hz, duty rate
    pi.hardware_PWM(gppin_acc, PWM_Hz, int(Ref_Spd / 100.0 * 1000000) )
    # Steering control : GPIO13: Hz, duty rate
    pi.hardware_PWM(gppin_str, PWM_Hz, int(Ref_Str / 100.0 * 1000000) )
    time.sleep(1)

print("to end...")

# Set neutral 
pi.hardware_PWM(gppin_acc, PWM_Hz, PWM_NeutralSpd )
pi.hardware_PWM(gppin_str, PWM_Hz, PWM_NeutralStr )

time.sleep(1)

# For stopping PWM. 
# For Tamiya-system, RC car may alarm when PWM was not input.
# Keep continue providing neutral position without stopping.
# PWMを止める場合は下記を有効にする．
# タミヤサーボシステムの場合，PWMが切れるとエラー音がなるのでNeutralPositionにして継続する
# pi.stop()

print("finish.")
