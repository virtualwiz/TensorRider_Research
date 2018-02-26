from sys import exit
import pygame
import time

deadzone = 0.1

class Car:
    def __init__(self):
        self.speed = 0
        self.acceleration = -5
        self.direction = 0
        self.differential = 20

def Controller_DeadZoneJudgment(rawData):
    if(abs(rawData) <= deadzone):
        rawData = 0
    return rawData

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

while True:
    pygame.event.pump()
    stickVal_Acc = Controller_DeadZoneJudgment(controller.get_axis(1))
    stickVal_Dir = Controller_DeadZoneJudgment(controller.get_axis(2))
    rider.speed += rider.acceleration * stickVal_Acc
    if rider.speed > 100:
        rider.speed = 100
    elif rider.speed < 0:
        rider.speed = 0
    rider.direction = stickVal_Dir * rider.differential
    time.sleep(0.1)
    print("speed:",round(rider.speed,3),"direction",round(rider.direction,3))

