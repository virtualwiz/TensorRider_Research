import threading
import time
from sys import exit

BCN_LIGHT_PERIOD = 0.1
BCN_LIGHT_PERIOD_LONG = 0.2
BCN_STOP_INTERVAL = 2
BCN_RUN_INTERVAL = 0.5

bcnStatus = 0

class Beacon:
    def __init__(self):
        self.status = 0

    def singleFlash():
        self.status = 1
        time.sleep(BCN_LIGHT_PERIOD)
        self.status = 0

    def doubleFlash():
        for cycle in range(0,1):
            self.status = 1
            time.sleep(BCN_LIGHT_PERIOD)
            self.status = 0
            time.sleep(BCN_LIGHT_PERIOD)

    def longFlash():
        self.status = 1
        time.sleep(BCN_LIGHT_PERIOD_LONG)
        self.status = 0

    def init():
        global beaconThread
        if bcnStatus == 0:
            beaconThread = threading.Timer(BCN_STOP_INTERVAL, self.init)
            beaconThread.start()
        # elif bcnStatus == 1:
        #     beaconThread = threading.Timer(BCN_STOP_INTERVAL, self.init)
        #     beaconThread.start()
        # elif bcnStatus == 2:
        #     beaconThread = threading.Timer(BCN_RUN_INTERVAL, self.init)
        #     beaconThread.start()

        # if bcnStatus == 0:
        #     self.singleFlash()
        # elif bcnStatus == 1:
        #     self.doubleFlash()
        # elif bcnStatus == 2:
        #     self.longFlash()

flashlight = Beacon()

beaconThread = threading.Timer(BCN_STOP_INTERVAL, flashlight.init)
beaconThread.start()

while True:
    print(flashlight.status)
    time.sleep(0.02)