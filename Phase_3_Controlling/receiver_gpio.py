import RPi.GPIO as io
import socket
import threading
from time import ctime,sleep

addr=('',51423)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(addr)

MOTOR_IO_LEFT = 13
MOTOR_IO_RIGHT = 15
MOTOR_PWM_FREQUENCY = 640

io.setmode(io.BOARD)
io.setup(MOTOR_IO_LEFT, io.OUT)
io.setup(MOTOR_IO_RIGHT, io.OUT)
MotorPwmL = io.PWM(MOTOR_IO_LEFT, MOTOR_PWM_FREQUENCY)
MotorPwmR = io.PWM(MOTOR_IO_RIGHT, MOTOR_PWM_FREQUENCY)
MotorPwmL.start(0)
MotorPwmR.start(0)


def Range_Limiter(val,range_min,range_max):
    if val > range_max:
        val = range_max
    elif val < range_min:
        val = range_min
    return val

class Car:
    def __init__(self):
        self.speed = 0
        self.direction = 0
        self.pwmDutyLeft = 0
        self.pwmDutyRight = 0

    def writeMotor(self):
        # self.pwmDutyLeft = self.speed + (self.direction * (self.speed / 100))
        # self.pwmDutyRight = self.speed - (self.direction * (self.speed / 100))
        # self.pwmDutyLeft = Range_Limiter(self.pwmDutyLeft, 0, 100)
        # self.pwmDutyRight = Range_Limiter(self.pwmDutyRight, 0, 100)
        self.pwmDutyLeft = self.speed + self.direction
        self.pwmDutyRight = self.speed - self.direction
        self.pwmDutyLeft = Range_Limiter(self.pwmDutyLeft, 0, 100)
        self.pwmDutyRight = Range_Limiter(self.pwmDutyRight, 0, 100)
        # print(self.pwmDutyLeft, self.pwmDutyRight)
        MotorPwmL.ChangeDutyCycle(self.pwmDutyLeft)
        MotorPwmR.ChangeDutyCycle(self.pwmDutyRight)
    

rider = Car()

def Controller_ReceiveAndWrite():
    while True:
        data,addr = s.recvfrom(2048)
        data = str(data)
        # print(data)
        rider.speed = int(float(data[0:data.find(r',')]))
        rider.direction = int(float(data[data.find(r',') + 1:-1] + data[-1]))
        rider.writeMotor()
        sleep(0.1)

ControlThread = threading.Thread(target = Controller_ReceiveAndWrite)
ControlThread.start()
