#from Adafruit_PWM_Servo_Driver import PWM
import socket


localIP     = ""
localPort   = 8080
bufferSize  = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")



    
ROBOT_NAME = "Thursday" #Im stupid
PWM_FREQ = 50
# LEFT_MOT = 0
LEFT_MOT = 0
# RIGHT_MOT = 1
RIGHT_MOT = 1
# LEFT_MANIP = 4
# RIGHT_MANIP = 5

#pwm = PWM(0x40)

leftMtr = 0
rightMtr = 0

def getData():
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    data = str(message).split(":")
    return [float(data[0]), float(data[1])]
    
'''
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
'''
while True:
    print(getData())
    #setServoPulse(LEFT_MOT, leftMtr)
    #setServoPulse(RIGHT_MOT, rightMtr)

