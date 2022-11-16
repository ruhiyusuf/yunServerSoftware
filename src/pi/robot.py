from robot_drive import RobotDrive
from motor_controller import MotorController
class Robot:
    def __init__(self):
        self.l_drive_mot = MotorController(0)
        self.r_drive_mot = MotorController(1)
        self.rob_drive = RobotDrive(self.l_drive_mot,self.r_drive_mot)


    def robot_control(self,left_y,right_x,left_trigger,right_trigger,left_shoulder,right_shoulder):
        self.rob_drive.drive(left_y,right_x)
