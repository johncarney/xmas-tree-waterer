#!/user/bin/env python3.10

from gpiozero import DistanceSensor, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

import time

factory = PiGPIOFactory(host="localhost")

pump = OutputDevice(4, active_high=True, initial_value=False, pin_factory=factory)

reservoir = DistanceSensor(trigger=23, echo=24, pin_factory=factory)
planter = DistanceSensor(trigger=20, echo=21, pin_factory=factory)

min_reservoir_level = 11 / 100
max_reservoir_level = 15 / 100

min_planter_level = 5 / 100
max_planter_level = 3 / 100

def reservoir_empty():
    return reservoir.distance > min_reservoir_level

def reservoir_full():
    return reservoir.distance < max_reservoir_level

def planter_empty():
    return planter.distance > min_planter_level

def planter_full():
    return planter.distance < max_planter_level

def report_depths():
    print(f"Reservoir depth: {round(reservoir.distance * 100, 2)}cm")
    print(f"Planter depth:   {round(planter.distance * 100, 2)}cm")

def fill_pot():
    pump.on()
    while not(reservoir_empty() or planter_full()):
        report_depths()
        time.sleep(0.5)
    pump.off()

try:
    while True:
        report_depths()
        time.sleep(5)
        if planter_empty():
            fill_pot()

finally:
    pump.off()
