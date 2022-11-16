from Adafruit_PWM_Servo_Driver import PWM
import time
from transform import Transform

class MotorController:
    pwm_controller = PWM(0x40)
    def __init__(self, chan, pwm_freq = 50, pwm_min_pulse = 1000, pwm_idle_pulse = 1500, pwm_max_pulse = 2000):
        self.channel = chan
        self.pwm_frequency = pwm_freq
        self.pwm_min = pwm_min_pulse
        self.pwm_idle = pwm_idle_pulse
        self.pwm_max = pwm_max_pulse
        self.watchdog = time.time()

    def set_pwm_configs(self, pwm_min_pulse,pwm_idle_pulse,pwm_max_pulse):
        self.pwm_min = pwm_min_pulse
        self.pwm_idle = pwm_idle_pulse
        self.pwm_max = pwm_max_pulse

    # set output from 0 to 255, with 0 behing full reverse, 255 full forward and 127 neutral
    def set_scaled_output(self, value):
        pulse = Transform.map_range(value,0,255,self.pwm_min,self.pwm_max)
        pulseLength = 1000000  # 1,000,000 us per second
        pulseLength /= self.pwm_frequency  # 50 Hz
        # print "%d us per period" % pulseLength
        pulseLength /= 4096  # 12 bits of resolution
        # print "%d us per bit" % pulseLength
        pulse /= pulseLength
        # print "%d tick" % pulse
        MotorController.pwm_controller.setPWM(self.channel, 0, pulse)
        self.watchdog = time.time()
    
    def set_raw_output(self, value):
        pulseLength = 1000000  # 1,000,000 us per second
        pulseLength /= self.pwm_frequency  # 50 Hz
        # print "%d us per period" % pulseLength
        pulseLength /= 4096  # 12 bits of resolution
        # print "%d us per bit" % pulseLength
        value /= pulseLength
        # print "%d tick" % pulse
        MotorController.pwm_controller.setPWM(self.channel, 0, value)
        self.watchdog = time.time()
