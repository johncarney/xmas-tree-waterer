from gpiozero    import DistanceSensor
from dataclasses import dataclass

@dataclass
class ContainerSensorLevels:
    min:   float
    max:   float
    low:   float = None
    floor: float = None

    def __post_init__(self):
        if self.floor is None:
            self.floor = self.min
        if self.low is None:
            self.low = self.min

    def level(self, distance):
        return(self.floor - distance)

    def is_dry(self, distance):
        return(distance >= self.floor)

    def is_empty(self, distance):
        return(distance >= self.min)

    def is_low(self, distance):
        return(distance >= self.low)

    def is_full(self, distance):
        return(distance <= self.max)

class Container:
    def __init__(self, pins, levels, volumes=None, pin_factory=None):
        self._sensor = DistanceSensor(pin_factory=pin_factory, **pins)
        self._levels = ContainerSensorLevels(**levels)
        self._volumes = volumes

    @property
    def _distance(self):
        return self._sensor.distance

    @property
    def level(self):
        return(self._levels.level(self._distance))

    @property
    def is_dry(self):
        return(self._levels.is_dry(self._distance))

    @property
    def is_empty(self):
        return(self._levels.is_empty(self._distance))

    @property
    def is_low(self):
        return(self._levels.is_low(self._distance))

    @property
    def is_full(self):
        return(self._levels.is_full(self._distance))
