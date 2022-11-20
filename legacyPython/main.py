import pygame
from pygame.locals import *
from UDP import sendUDP
import time

pygame.init()
#Attach joysticks before running
JOYSTICKS = [0]
RPI_IPS = ["192.168.86.33"]

jstick_list = []
for i in JOYSTICKS:
    jstick_list.append(pygame.joystick.Joystick(i))



while True:
    time.sleep(.005)
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()

    if jstick_list[0].get_button(0):
        print("stopped")
        break
    else:
        for i in range(0, len(jstick_list)):
            x = round(jstick_list[i].get_axis(2), 3)
            y = round(-jstick_list[i].get_axis(1), 3)
            msg = str(x) + ":" + str(y)
            print(msg)
            sendUDP(msg, IP = RPI_IPS[i], port = 8080)