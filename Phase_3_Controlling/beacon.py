import threading
import time
from sys import exit

BCN_LIGHT_PERIOD = 0.1
BCN_LIGHT_PERIOD_LONG = 0.5
BCN_STOP_INTERVAL = 2
BCN_RUN_INTERVAL = 1

bcnStatus = 0

def flashBeacon():
    mode = bcnStatus
    if mode == 0:
        print("on")
        time.sleep(BCN_LIGHT_PERIOD)
        print("off")
    elif mode == 1:
        for cycle in range(2):
            print("on")
            time.sleep(BCN_LIGHT_PERIOD)
            print("off")
            time.sleep(BCN_LIGHT_PERIOD)
    elif mode == 2:
        print("on")
        time.sleep(BCN_LIGHT_PERIOD_LONG)
        print("off")

def indicator_Write():
    flashBeacon()
    global beaconThread
    if bcnStatus == 0:
        beaconThread = threading.Timer(BCN_STOP_INTERVAL, indicator_Write)
        beaconThread.start()
    elif bcnStatus == 1:
        beaconThread = threading.Timer(BCN_STOP_INTERVAL, indicator_Write)
        beaconThread.start()
    elif bcnStatus == 2:
        beaconThread = threading.Timer(BCN_RUN_INTERVAL, indicator_Write)
        beaconThread.start()

beaconThread = threading.Timer(BCN_STOP_INTERVAL, indicator_Write)
beaconThread.start()
