# Speed & Steering command class for TAMIYA Finespec RC Servo using pigpio 
#
# Copyright (c) 2023 MODECO
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

import pigpio

class TamiyaRCPWM:
    """ PWM command module for Tamiya RC Servo """
    pi = pigpio.pi()

    PWM_SPD_NEUTRAL = 10  # Center value for stopping
    #PWM_SPD_FWDSTART = 10
    PWM_SPD_FWDMAX = 9    # Normal cruising speed value 
    #PWM_SPD_FWDSTART = 10
    PWM_SPD_BCKMAX = 11   # Normal backward speed value
 
    PWM_STR_NEUTRAL = 10
    #PWM_SPD_FWDSTART = 10
    PWM_STR_LFTMAX = 8
    #PWM_SPD_FWDSTART = 10
    PWM_STR_RGTMAX = 11

    PWM_SPD_PIN = 12 # 12&13 are available for hardware PWM
    PWM_STR_PIN = 13 
    PWM_Hz = 70   # 70 is recommended for Tamiya Servo
    PWM_SAFE_MIN = 7.50   # safety limit for PWM duty ratio in percent
    PWM_SAFE_MAX = 13.00  # safety limit for PWM duty ratio in percent

    def __init__(self, STR_PIN = 13, SPD_PIN = 12):
        # start hardware PWM for 12/13 pints
        # pi = pigpio.pi()
        PWM_SPD_PIN = SPD_PIN
        PWM_STR_PIN = STR_PIN
        self.pi.set_mode(PWM_SPD_PIN, pigpio.OUTPUT)
        self.pi.set_mode(PWM_STR_PIN, pigpio.OUTPUT)

    # compute command value for duty rate
    # 1000,000 = 100% in hardware PWM with pigpio
    def calcDutyDigit( dutyRateInPercent ):
        duty = dutyRateInPercent / 100.0 * 1000000

    # Set PWM with original API (100% duty ratio = 1000,000 duty_digit)
    def setPWMRaw( self, pin, hz, duty_digit ):
        self.pi.hardware_PWM(pin, hz, duty_digit)

    # Set PWM ( dutyInPercent = [0-100] % )
    def setPWM( self, pin, hz, dutyInPercent ):
        self.setPWMRaw( pin, hz, self.calcDutyDigit(dutyInPercent) )

    # Set speed with duty ratio (dutyInPercent = [0-100] in %)
    def setSpeedDutyRatio (self, dutyInPercent ):
        # for safety limit
        if dutyInPercent > self.PWM_SAFE_MAX:
            dutyInPercent = self.PWM_SAFE_MAX
        if dutyInPercent < self.PWM_SAFE_MIN:
            dutyInPercent = self.PWM_SAFE_MIN
        self.setPWM( self.PWM_SPD_PIN, self.PWM_HZ, dutyInPercent )
        return dutyInPercent

    # Set steering with duty ratio (dutyInPercent = [0-100] in %)
    def setSteeringDutyRatio (self, dutyInPercent ):
        # for safety limit
        if dutyInPercent > self.PWM_SAFE_MAX:
            dutyInPercent = self.PWM_SAFE_MAX
        if dutyInPercent < self.PWM_SAFE_MIN:
            dutyInPercent = self.PWM_SAFE_MIN
        self.setPWM( self.PWM_STR_PIN, self.PWM_HZ, dutyInPercent )
        return dutyInPercent



        

