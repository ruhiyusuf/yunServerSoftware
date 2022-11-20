#from Adafruit_PWM_Servo_Driver import PWM
import socket
import time
import threading



localIP     = ""
localPort   = 8080
bufferSize  = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")



TIME_DELAY = 5
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
        m_left = data[0]
        m_right = data[1]
        #transform code Here
        #setServoPulse(LEFT_MOT, leftMtr)
        #setServoPulse(RIGHT_MOT, rightMtr)
    


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
                print("Data reception went overtime!")
                break

m_watch = threading.Thread(target = motor_watch, args = ())

m_thread.start()
m_watch.start()

    
    
    

