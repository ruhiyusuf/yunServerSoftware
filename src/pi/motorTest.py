from Adafruit_PWM_Servo_Driver import PWM
from transform import Transform
import socket
import select
import sys
import time
import atexit
import queue
from threading import Thread
import configparser
from smbus import SMBus


ROBOT_NAME = "Thursday" #Im stupid
PWM_FREQ = 50
# LEFT_MOT = 0
LEFT_MOT = 0
# RIGHT_MOT = 1
RIGHT_MOT = 1
# LEFT_MANIP = 4
# RIGHT_MANIP = 5

pwm = PWM(0x40)

leftMtr = 0
rightMtr = 0



def setServoPulse(channel, pulse):
    pulseLength = 1000000  # 1,000,000 us per second
    pulseLength /= PWM_FREQ  # 50 Hz
    # print "%d us per period" % pulseLength
    pulseLength /= 4096  # 12 bits of resolution
    # print "%d us per bit" % pulseLength
    pulse /= pulseLength
    # print "%d tick" % pulse
    pwm.setPWM(channel, 0, int(pulse)) # change: casted pulse to int

pwm.setPWMFreq(50)
setServoPulse(LEFT_MOT, leftMtr)
setServoPulse(RIGHT_MOT, rightMtr)
