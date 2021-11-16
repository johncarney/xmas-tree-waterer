#!/user/bin/env python3

from gpiozero import OutputDevice, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

import time

factory = PiGPIOFactory(host="localhost")
pump = OutputDevice(4, active_high=True, initial_value=False, pin_factory=factory)
reservoir = DistanceSensor(trigger=20, echo=21, max_distance=3, pin_factory=factory)
planter = DistanceSensor(trigger=5, echo=6, max_distance=3, pin_factory=factory)

min_reservoir_level = 10 / 100
max_reservoir_level = 15 / 100

min_planter_level = 10 / 100
max_planter_level = 15 / 100

def reservoir_empty():
    return reservoir.distance > min_reservoir_level

def reservoir_full():
    return reservoir.distance < max_reservoir_level

def planter_empty():
    return planter.distance > min_planter_level

def planter_full():
    return planter.distance < max_planter_level

def fill_pot():
    pump.on()
    while not(reservoir_empty() or planter_full()):
        time.sleep(1)
        print(f"Planter depth: {round(planter.distance * 100, 2)}cm")
    pump.off()

try:
    while True:
        time.sleep(10)
        if planter_empty():
            fill_pot()
except KeyboardInterrupt:
    print()
