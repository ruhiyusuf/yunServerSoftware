import pygame
from pygame.locals import *

pygame.init()
jstick = pygame.joystick.Joystick(0)
#A = 0, B = 1, X = 2, Y = 3
while True:
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()
    if (jstick.get_button(0)):
        print(0)
    if (jstick.get_button(1)):
        print(1)
    if (jstick.get_button(2)):
        print(2)
    if (jstick.get_button(3)):
        print(3)
    