from gpiozero    import DistanceSensor
from dataclasses import dataclass

@dataclass
class ContainerLevels:
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

class ContainerVolumeMap:
    def __init__(self, map):
        if map is None:
            self._map = None
        else:
            self._map = sorted(map)

    def volume(self, distance):

        pass

class Container:
    def __init__(self, pins, levels, volume_map=None, pin_factory=None):
        self._sensor = DistanceSensor(pin_factory=pin_factory, **pins)
        self._levels = ContainerLevels(**levels)
        self._volume_map = ContainerVolumeMap(volume_map)

    @property
    def _distance(self):
        return self._sensor.distance * 100

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
