import pygame
from pygame.locals import *
from UDP import sendUDP
import time

pygame.init()

joystick = pygame.joystick.Joystick(0)

while True:
    time.sleep(.005)
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()

    if joystick.get_button(0):
        print("stopped")
        break
    else:
        x = round(joystick.get_axis(2), 3)
        y = round(-joystick.get_axis(1), 3)
        msg = str(x) + ":" + str(y)
        print(msg)
        sendUDP(msg, IP = "192.168.86.33", port = 8080)