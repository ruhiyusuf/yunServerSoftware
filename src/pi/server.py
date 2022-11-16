from Adafruit_PWM_Servo_Driver import PWM
from transform import Transform
import socket
import select
import sys
import time
import atexit
from Queue import Queue
from robot import Robot
from motor_controller import MotorController
from threading import Thread
import ConfigParser

# network related variables
PORT = 2380  # Game host port
BROADCAST_PORT = 2367  # Broadcast port
BROADCAST_IP = ''
LOCAL_IP = ''

# timouts for respective interval timers
KEEP_ALIVE_TIMEOUT = 2
NAME_BROADCAST_TIMEOUT = 1
WATCHDOG_DELAY = 0.2

# thread communication queues
broadcastQueue = Queue()
serialRealTimeQueue = Queue()
networkRealTimeQueue = Queue()
networkQueue = Queue()



config = ConfigParser.ConfigParser()
config.read('/home/pi/yunServerSoftware/src/pi/config.ini')

# change this to the relevant team name when the script is loaded to the yun
ROBOT_NAME = config.get('Main','TeamName')
PWM_FREQ = 50
LEFT_MOT = 0
RIGHT_MOT = 1
LEFT_MANIP = 4
RIGHT_MANIP = 5

pwm = PWM(0x40)


def setServoPulse(channel, pulse):
    pulseLength = 1000000  # 1,000,000 us per second
    pulseLength /= PWM_FREQ  # 50 Hz
    # print "%d us per period" % pulseLength
    pulseLength /= 4096  # 12 bits of resolution
    # print "%d us per bit" % pulseLength
    pulse /= pulseLength
    # print "%d tick" % pulse
    pwm.setPWM(channel, 0, pulse)


# loging wrapper function
def logWrite(strng):
    log.write("[" + str(time.time()) + "]" + strng + "\n")
    print strng


# Error log file, overwtite file from last reset
logFile = "./elog_" + str(time.time()) + ".txt"
try:
    log = open(logFile, "w")
except Exception as f:
    print "Uhhh... check that your hard drive isn't on fire!"
    sys.exit(1)
else:
    logWrite("log File" + logFile)


# threaded function that listens for broadcasts from host.
def broadcastListener():
    bCastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bCastSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bCastSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        bCastSock.bind((BROADCAST_IP, BROADCAST_PORT))
    except socket.error as msg:
        bCastSock.close()
        logWrite('Broadcast bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] + "\n")
        sys.exit(1)

    while True:
        readReady = select.select([bCastSock], [], [], 0.02)
        if readReady[0]:
            data, sender = bCastSock.recvfrom(1500)
            # check that the datagram is a alive packet
            if data == sender[0]:
                broadcastQueue.put(sender)
        time.sleep(.05)


# serial communication thread
def pwmControlThread():
    # setup arduino serial comm
    robot = Robot()
    # thread main loop
    while True:
        time.sleep(.005)
        # check for data that needs to be bridged to arduino
        dataFlag = True
        if not serialRealTimeQueue.empty():
            data = serialRealTimeQueue.get()
        else:
            dataFlag = False

        # if data was recieved parse and update pwm hat
        if dataFlag:
            data = data[5:-1]
            print data
            data_nums = [int(x) for x in data.split(':') if x.strip()]
            robot.robot_control(data_nums[0],data_nums[1],data_nums[2],data_nums[3], data_nums[4] == 255, data_nums[4] == 0)

        for mc in dir(robot):
            if isinstance(mc,MotorController):
                if mc.watchdog + WATCHDOG_DELAY < time.time():
                    mc.set_scaled_output(127)

def networkComThread():
    
    # create socket to recieve from host
    netSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    netSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        netSock.bind((LOCAL_IP, PORT))
    except socket.error as msg:
        logWrite('Broadcast bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit(1)

    # main thead loop
    while True:
        # wait for data from broadcast listener thread
        logWrite("Waiting for host.")
        host = broadcastQueue.get(True)

        # run loop while we continue to get broadcast packets from the host
        fKeepAlive = True
        keepAliveTimer = time.time()
        nameBroadcastTimer = time.time()
        logWrite("Found Host.")
        while fKeepAlive:
            time.sleep(.005)
            if not broadcastQueue.empty():
                while not broadcastQueue.empty():
                    broadcastQueue.get()
                keepAliveTimer = time.time()
            # if we haven't recieved a keep alive packet in a while kill the connection
            if time.time() - keepAliveTimer > KEEP_ALIVE_TIMEOUT:
                fKeepAlive = False
                logWrite("Connection Died due to timeout")
                break

            # check for data from host and pass it to the serial thread
            ready = select.select([netSock], [], [], 0.005)
            if ready[0]:
                bridgeData, senderAddr = netSock.recvfrom(1024)
                if bridgeData:
                    if senderAddr[0] == host[0]:
                        serialRealTimeQueue.put(bridgeData)

                    # check serial queue and pass to the host if data is available
            if not networkQueue.empty():
                serialData = networkQueue.get()
                netSock.sendto('DBG:' + ROBOT_NAME + ':' + serialData, (host[0], PORT))

            # broadcast name on interval
            if time.time() - nameBroadcastTimer > NAME_BROADCAST_TIMEOUT:
                nameBroadcastTimer = time.time()
                netSock.sendto('ROB:' + ROBOT_NAME, (host[0], PORT))
                logWrite("Sent robot name.")


# cleanup function
def cleanup():
    logWrite('cleanup')


# Main program start
pwmThread = Thread(target=pwmControlThread, args=())
broadcastThread = Thread(target=broadcastListener, args=())
networkThread = Thread(target=networkComThread, args=())

pwmThread.daemon = True
broadcastThread.daemon = True
networkThread.daemon = True

pwmThread.start()
broadcastThread.start()
networkThread.start()

atexit.register(cleanup)

while True:
    if not pwmThread.isAlive():
        pwmThread.run()
        logWrite("Restarting serial thread")
    if not broadcastThread.isAlive():
        broadcastThread.run()
        logWrite("Restarting broadcast listener thread")
    if not networkThread.isAlive():
        networkThread.run()
        logWrite("Restarting network thread")

    time.sleep(1)
