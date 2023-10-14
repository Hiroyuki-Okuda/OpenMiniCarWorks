# Speed & Steering command class for TAMIYA Finespec RC Servo using pigpio 
#
# Copyright (c) 2023 MODECO
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

import pigpio

class TamiyaRCPWM:
    """ PWM command module for Tamiya RC Servo """



    def __init__(self, STR_PIN = 13, SPD_PIN = 12):
        # start hardware PWM
        pi = pigpio.pi()
        pi.set_mode(SPD_PIN, pigpio.OUTPUT)
        pi.set_mode(STR_PIN, pigpio.OUTPUT)

    def setPWM( PIN, HZ, DUTY ):
        pi.hardware_PWM(PIN, HZ, DUTY)

        

