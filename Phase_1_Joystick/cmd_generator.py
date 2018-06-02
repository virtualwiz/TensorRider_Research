from sys import exit
import pygame
# import time
import threading

# CONFIG
deadzone = 0.1
controllerReadInterval = 0.1
# END OF CONFIG

class Car:
    def __init__(self):
        self.speed = 0
        self.acceleration = -5
        self.direction = 0
        self.differential = 20

def Controller_DeadZoneCancellation(rawData):
    if(abs(rawData) <= deadzone):
        rawData = 0
    return rawData

def Range_Limiter(val,min,max):
    if val > max:
        val = max
    elif val < min:
        val = min
    return val

def Controller_Read():
    global controllerReadTimer
    controllerReadTimer = threading.Timer(controllerReadInterval, Controller_Read)
    controllerReadTimer.start()

    pygame.event.pump()
    stickVal_Acc = Controller_DeadZoneCancellation(controller.get_axis(1))
    stickVal_Dir = Controller_DeadZoneCancellation(controller.get_axis(2))
    rider.speed += rider.acceleration * stickVal_Acc
    rider.speed = Range_Limiter(rider.speed, 0, 100)
    rider.direction = stickVal_Dir * rider.differential
    if controller.get_button(6) + controller.get_button(7) == 2:
        rider.speed = 0 #Emergency Stop
    print("speed:",round(rider.speed,3),"direction",round(rider.direction,3))


pygame.joystick.init()
pygame.display.init()

if pygame.joystick.get_count() == 1:
    controller = pygame.joystick.Joystick(0)
    print("Using controller:",controller.get_name())
elif pygame.joystick.get_count() == 0:
    print("Controller Not Found.")
    exit()
else:
    print("Multiple controllers found.")
    exit()

controller.init()
print("Controller initialized.")

rider = Car()
controllerReadTimer = threading.Timer(controllerReadInterval, Controller_Read)
controllerReadTimer.start()




# while True:
#     pygame.event.pump()
#     stickVal_Acc = Controller_DeadZoneCancellation(controller.get_axis(1))
#     stickVal_Dir = Controller_DeadZoneCancellation(controller.get_axis(2))
#     rider.speed += rider.acceleration * stickVal_Acc
#     if rider.speed > 100:
#         rider.speed = 100
#     elif rider.speed < 0:
#         rider.speed = 0
#     rider.direction = stickVal_Dir * rider.differential
#     time.sleep(0.1)
#     print("speed:",round(rider.speed,3),"direction",round(rider.direction,3))

