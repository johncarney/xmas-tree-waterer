from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from dataclasses import dataclass
import serial


@dataclass
class GenericSensor:
    trigger: int
    echo:    int

    def __post_init__(self):
        pin_factory = PiGPIOFactory(host="localhost")
        self._impl = DistanceSensor(trigger=self.trigger, echo=self.echo, pin_factory=pin_factory)

    def distance(self):
        return(self._impl.distance * 10.0)


@dataclass
class US100Sensor:
    port: str

    def __post_init__(self):
        self._serial_port = serial.Serial(self.port, baudrate=9600, timeout=2)

    def distance(self):
        self._serial_port.write(b"\x55")
        rsp = self._serial_port.read(2)
        return(float(rsp[0] * 256 + rsp[1]))


def sensor(config):
    if "port" in config:
        return(US100Sensor(**config))
    elif "trigger" in config and "echo" in config:
        return(GenericSensor(**config))
    else:
        return(None)
