import time
class RobotDrive:
    L_STICK_DEADZONE = 17
    R_STICK_DEADZONE = 17
    

    def __init__(self,left_mot,right_mot):
        self.l_mot = left_mot
        self.r_mot = right_mot
        self.invert_left = True
        self.invert_right = False

    
    def drive(self,left_stick_y, right_stick_x):
        if 127 - RobotDrive.L_STICK_DEADZONE <= left_stick_y <= 127 + RobotDrive.L_STICK_DEADZONE :
            left_stick_y = 127
        if 127 - RobotDrive.R_STICK_DEADZONE <= right_stick_x <= 127 + RobotDrive.R_STICK_DEADZONE :
            right_stick_x = 127

        if self.invert_left:
            leftMtr = 255 - left_stick_y
        else:
            leftMtr = left_stick_y
        if self.invert_right:
            rightMtr = 255 - left_stick_y
        else :
            rightMtr = left_stick_y

        if self.invert_left:
            leftMtr += right_stick_x - 127
        else:
            leftMtr -= right_stick_x - 127
        if self.invert_right:
            rightMtr -= right_stick_x - 127
        else:
            rightMtr += right_stick_x - 127
        self.l_mot.set_scaled_output(leftMtr)
        self.r_mot.set_scaled_output(rightMtr)


d = RobotDrive(0,1)
d.drive(127,127)
