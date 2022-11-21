import pygame
from pygame.locals import *
from UDP import sendUDP
import time
import threading

pygame.init()
#Attach joysticks before running
JOYSTICKS = [0]
RPI_IPS = ["192.168.86.33"]

jstick_list = []
for i in JOYSTICKS:
    jstick_list.append(pygame.joystick.Joystick(i))

stop_threads = False

def send_values(jstick, i):
    global stop_threads
    while True:
        time.sleep(.005)
        if stop_threads:
            break
        if jstick.get_button(2):
            #print("stopped")
            break
        else:
            x = round(jstick.get_axis(2), 3)
            y = round(-jstick.get_axis(1), 3)
            manip1 = round(jstick.get_axis(4), 3)
            manip2 = round(jstick.get_axis(5), 3)
            a_press = int(jstick.get_button(0))
            b_press = int(jstick.get_button(1))
            msg = str(x) + ":" + str(y) + ":" + str(manip1) + ":" + str(manip2) + ":" + str(a_press) + ":" + str(b_press)
            #print(msg)
            sendUDP(msg, IP = RPI_IPS[i], port = 8080)

thread_list = []
for i in range(0, len(jstick_list)):
    thread_list.append(threading.Thread(target = send_values, args = (jstick_list[i], i)))


for i in range(0, len(thread_list)):
    thread_list[i].start()

while True:
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            stop_threads = True
            for i in thread_list:
                i.join()
            pygame.quit()
            exit()
'''
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
            manip1 = round(jstick_list[i].get_axis(4), 3)
            manip2 = round(jstick_list[i].get_axis(5), 3)
            msg = str(x) + ":" + str(y) + ":" + str(manip1) + ":" + str(manip2)
            print(msg)
            sendUDP(msg, IP = RPI_IPS[i], port = 8080)
'''