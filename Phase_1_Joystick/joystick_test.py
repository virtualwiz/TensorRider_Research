from sys import exit
import pygame
import time

pygame.joystick.init()
pygame.display.init()

if pygame.joystick.get_count() == 1:
    controller = pygame.joystick.Joystick(0)
    print("Controller:",controller.get_name(),"Found.")
else:
    print("No controller or multiple controllers found.")
    exit()

print("Press ENTER to begin.")
input()

controller.init()
print("Controller initialized.")

while True:
    pygame.event.pump()
    for axis in range(controller.get_numaxes()):
        print(round(controller.get_axis(axis),3),end="\t")
    print("\n")
    
    for button in range(controller.get_numbuttons()):
        print(controller.get_button(button),end="\t")
    print("\n")
    
    time.sleep(0.2)

