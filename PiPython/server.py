#from Adafruit_PWM_Servo_Driver import PWM
import socket
import time
import threading
from transform import *


localIP     = ""
localPort   = 8080
bufferSize  = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


teams = ["Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_DELAY = 5
ROBOT_NAME = str(input("Enter team name:")) #Im stupid
while not(ROBOT_NAME in teams):
    ROBOT_NAME = str(input("Enter valid team name:"))
PWM_FREQ = 50


LEFT_MOT = int(input("Left Mot(0):"))
RIGHT_MOT = int(input("Right Mot(1):"))
LEFT_MANIP = int(input("Left Manip(4):")) #One manipulator for Intake/Rotation
RIGHT_MANIP = int(input("Right Manip(5):")) #Second manipualtor for intake/rotation

#pwm = PWM(0x40)

leftMtr = 0
rightMtr = 0

def getData():
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    data = str(message).split(":")
    print(data)
    #print(data[0][2:])
    data[0] = data[0][2:]
    data[len(data)-1] = data[len(data)-1][:-1]
    return list(map(float, data)) #CHANGE PARSING HERE FOR FURTHER DATA INPUTS, last data element [:-1]
    
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
m_left = 0
m_right = 0
last_left = 0
last_right = 0
last_time = time.time()
stop_thread = False


def motor_update():
    global m_left
    global m_right
    global last_left
    global last_right
    global last_time
    global stop_thread
    while True:
        if stop_thread:
            break
        data = getData()
        last_left = m_left
        last_right = m_right
        last_time = time.time()
        m_left = data[1]
        m_right = data[0]
        trigger_1 = data[2]
        trigger_2 = data[3]
        a_press = data[4]
        b_press = data[5]

        
        if ROBOT_NAME == "Tuesday":
            L, R, ML, MR = tuesdayTransform(m_left, m_right, trigger_1, trigger_2, a_press, b_press)
        elif ROBOT_NAME == "Wednesday":
            L, R, ML, MR = wednesdayTransform(m_left, m_right, trigger_1, trigger_2, a_press, b_press)
        elif ROBOT_NAME == "Thursday":
            L, R, ML, MR = thursdayTransform(m_left, m_right, trigger_1, trigger_2, a_press, b_press)
        elif ROBOT_NAME == "Friday":
            L, R, ML, MR = fridayTransform(m_left, m_right, trigger_1, trigger_2, a_press, b_press)
        else:
            print("no team name configured")
            L, R, ML, MR = 0, 0, 0, 0
        list = [L, R, ML, MR]
        print(list)
        #setServoPulse(LEFT_MOT, L)
        #setServoPulse(RIGHT_MOT, R)
        #setServoPulse(LEFT_MANIP, ML)
        #setServoPulse(RIGHT_MANIP, MR)
    


m_thread = threading.Thread(target=motor_update, args=(), daemon=True)



def motor_watch():
    global last_time
    global m_left
    global m_right
    global last_left
    global last_right
    global stop_thread
    while True:
        if ((time.time() - last_time) > TIME_DELAY):
            if ((last_left == m_left) and (last_right == m_right) and (last_left != 0.0) and (last_right != 0.0)):
                stop_thread = True
                #setServoPulse(LEFT_MOT, 0)
                #setServoPulse(RIGHT_MOT, 0)
                #setServoPulse(LEFT_MANIP, 0)
                #setServoPulse(RIGHT_MANIP, 0)
                print("Data reception went overtime!")
                break

m_watch = threading.Thread(target = motor_watch, args = ())

m_thread.start()
m_watch.start()

    
    
    

