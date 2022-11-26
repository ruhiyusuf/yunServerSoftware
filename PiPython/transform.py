#Scale controller x,y values in range(-1,1) to motor value from (1000, 2000)
#Direction switch at 1500
#
import math

MOTOR_MAX = 2000
MOTOR_MIN = 1000
MOTOR_IDLE = 1500
MOTOR_ZERO = 0
L_DEADZONE = 0.1
R_DEADZONE = 0.1

INTAKE_DIF = 100
ARM_DIF = 100


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def driveTransform(leftY, rightX):
    Lout = 0
    Rout = 0
    if (abs(leftY) < L_DEADZONE):
        leftY = 0
    if (abs(rightX) < R_DEADZONE):
        rightX = 0
        if leftY == 0:
            return 0, 0
    
    if (leftY >= 0):
        Lout = leftY + rightX
        Rout = leftY - rightX
    else:
        Lout = leftY - rightX
        Rout = leftY + rightX


    Lout = math.copysign(Lout ** 2, Lout)
    Rout = math.copysign(Rout ** 2, Rout)

    Lout = map_range(Lout, -1, 1, MOTOR_MIN, MOTOR_MAX)
    Rout = map_range(Rout, -1, 1, MOTOR_MIN, MOTOR_MAX)

    def bound(inp):
        if inp == 0:
            return 0
        if inp > MOTOR_MAX:
            return MOTOR_MAX
        elif inp < MOTOR_MIN:
            return MOTOR_MIN
        else:
            return inp
    Lout = bound(Lout)
    Rout = bound(Rout)
            
    return Lout, Rout
'''
def driveTransform(leftY, rightX, invert_right = False, invert_left = False): #Return motor value from leftY rightX
    lftMtr = 0
    rghtMtr = 0
    if (abs(leftY < L_DEADZONE)):
        leftY = MOTOR_ZERO
    else:
        leftY = map_range(leftY, -1, 1, MOTOR_MIN, MOTOR_MAX)
    
    if (abs(rightX < R_DEADZONE)):
        rightX = MOTOR_ZERO
    else:
        rightX = map_range(rightX, -1, 1, MOTOR_MIN, MOTOR_MAX)
        lftMtr = MOTOR_IDLE
        rghtMtr = MOTOR_IDLE
        if leftY > MOTOR_IDLE:
            if invert_left:
                rghtMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MAX, MOTOR_IDLE, MOTOR_MIN)
                lftMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MAX, MOTOR_IDLE, MOTOR_MAX)
            else:
                lftMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MAX, MOTOR_IDLE, MOTOR_MIN)
                rghtMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MAX, MOTOR_IDLE, MOTOR_MAX)

        elif leftY < MOTOR_IDLE:
            if invert_left:
                lftMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MIN, MOTOR_IDLE, MOTOR_MIN)
                rghtMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MIN, MOTOR_IDLE, MOTOR_MAX)
            else:
                rghtMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MIN, MOTOR_IDLE, MOTOR_MIN)
                lftMtr = map_range(leftY, MOTOR_IDLE, MOTOR_MIN, MOTOR_IDLE, MOTOR_MAX)

        if rightX > MOTOR_IDLE:
            turnRate = map_range(rightX, MOTOR_IDLE, MOTOR_MAX, MOTOR_IDLE, MOTOR_MAX)
            if invert_right:
                rghtMtr -= turnRate - MOTOR_IDLE
                lftMtr -= turnRate - MOTOR_IDLE
            else:
                lftMtr += turnRate - MOTOR_IDLE
                rghtMtr += turnRate - MOTOR_IDLE

        elif rightX < MOTOR_IDLE:
            turnRate = map_range(rightX, MOTOR_IDLE, MOTOR_MIN, MOTOR_IDLE, MOTOR_MIN)
            if invert_right:
                rghtMtr -= turnRate - MOTOR_IDLE
                lftMtr -= turnRate - MOTOR_IDLE
            else:
                lftMtr += turnRate - MOTOR_IDLE
                rghtMtr += turnRate - MOTOR_IDLE
        if lftMtr > MOTOR_MAX:
                lftMtr = MOTOR_MAX
        elif lftMtr < MOTOR_MIN:
            lftMtr = MOTOR_MIN

        if rghtMtr > MOTOR_MAX:
            rghtMtr = MOTOR_MAX
        elif rghtMtr < MOTOR_MIN:
            rghtMtr = MOTOR_MIN

    return lftMtr, rghtMtr
'''

def tuesdayTransform(leftY, rightX, triggerL, triggerR, a_press, b_press):
    manipL = 0
    manipR = 0
    m_left, m_right = driveTransform(leftY, rightX)
    triggerL += 1
    triggerR += 1
    if triggerR > 0.1:
        manipL = MOTOR_IDLE + ARM_DIF
    if triggerL > 0.1:
        manipL = MOTOR_IDLE - ARM_DIF
    if b_press:
        manipR = MOTOR_IDLE + INTAKE_DIF
    if a_press:
        manipR = MOTOR_IDLE - INTAKE_DIF

    return m_left, m_right, manipL, manipR

def wednesdayTransform(leftY, rightX, triggerL, triggerR, a_press, b_press):
    manipL = 0
    manipR = 0
    m_left, m_right = driveTransform(leftY, rightX)
    triggerL += 1
    triggerR += 1
    if triggerR > 0.1:
        manipL = MOTOR_IDLE + ARM_DIF
    if triggerL > 0.1:
        manipL = MOTOR_IDLE - ARM_DIF
    if b_press:
        manipR = MOTOR_IDLE + INTAKE_DIF
    if a_press:
        manipR = MOTOR_IDLE - INTAKE_DIF

    return m_left, m_right, manipL, 0

def thursdayTransform(leftY, rightX, triggerL, triggerR, a_press, b_press):
    manipL = 0
    manipR = 0
    m_left, m_right = driveTransform(leftY, rightX)
    triggerL += 1
    triggerR += 1
    if triggerR > 0.1:
        manipL = MOTOR_IDLE + ARM_DIF
    if triggerL > 0.1:
        manipL = MOTOR_IDLE - ARM_DIF
    if b_press:
        manipR = MOTOR_IDLE + INTAKE_DIF
    if a_press:
        manipR = MOTOR_IDLE - INTAKE_DIF

    return m_left, m_right, manipL, manipR

def fridayTransform(leftY, rightX, triggerL, triggerR, a_press, b_press): #Left, right, leftManip, rightManip
    manipL = 0
    manipR = 0
    m_left, m_right = driveTransform(leftY, rightX)
    triggerL += 1
    triggerR += 1
    if triggerR > 0.1:
        manipL = MOTOR_IDLE + ARM_DIF
    if triggerL > 0.1:
        manipL = MOTOR_IDLE - ARM_DIF
    if b_press:
        manipR = MOTOR_IDLE + INTAKE_DIF
    if a_press:
        manipR = MOTOR_IDLE - INTAKE_DIF

    return m_left, m_right, manipL, manipR



