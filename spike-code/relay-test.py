#!/user/bin/env python3

import RPi.GPIO as GPIO

import time

sensor = DistanceSensor(trigger=5, echo=6, max_distance=3)
try:
    while True:
        time.sleep(2)
        print(f"distance: {round(sensor.distance * 100, 2)}cm")

except KeyboardInterrupt:
    pass
