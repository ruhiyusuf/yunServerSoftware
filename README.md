# Yun Server Software
## Overview
This is the software to be run on the Arduino Yun for Soccer-bots. 
## Why custom control system?
Obviously the best training would be to have full FRC control systems for each soccer-bots team. However, several issues arise when doing so. The first and most obvious one is cost. Each FRC control system can cost upwards of $1000. With 6 teams and inexperienced members (i.e. more risk to break parts), it the cost to the team is quite substantial. Also, much of the functionality of the control system would remain unused as these robots are relatively simple, with most just being a simple drive base. 

The second reason is due to the difficulty of interfacing with six FRC control systems. Much of the FRC control system hardware is uncommon and thus not well documented. So connecting six of them to a single computer would probably be more difficult than using a couple of microcontrollers that are extremely well documented and widely used already outside of the competition.

Thus, it makes sense to find a solution that has the minimum requirements to make a working drive base with the possibility of adding simple sensors and a manipulator. The minimum specs for each robot control system are: Wifi, microcontroller, a couple of PWM ports, power delivery, and motor controllers. The Arduino Yun comes in here as it is a microcontroller with integrated WiFi capability. Power delivery is handled by FRC's last-gen power distribution board and motor controllers are a simple off the shelf part.

Because we chose to go with the Arduino Yun, custom software had to be written for it. This is the software to run the server which the Yuns connect to and allow for control of the robots. 

## Installation
- Needs python3
- pygame
- Adafruit Pihat
- Don't run the curl command

## Setup
- git clone
- git checkout separateUDP
- SSH to each pi & make sure they are on same wifi as laptop
- Get ip of each pi and enter them in rpi list in legacyPython/main.py
- Add numbers for joystick list in same file(should be 0 thru n)

On laptop:
- pip3 install pygame
- Connect all controllers before program starts
- python3 main.py
- **To end program on all devices press X on each controller**
- Each pi should stop motors after 5 seconds(5 is changeable)

On rpi:
- Customize transform funcs for each team
- Enter team name as string in server.py(Or enter on program start)
- python3 server.py
