from ..utils import VectorXY, FactorySequence


class RailProfile:
    def __init__(self, name):
        self.name = name
        self.rail_points = FactorySequence(RailProfilePoint)
        self.blade_points = FactorySequence(RailProfilePoint)


class RailProfilePoint:
    def __init__(self, values):
        self._location = VectorXY(values[:2])
        self._normal = VectorXY(values[2:4])
        self.mapping = values[4]

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, position):
        self._location = VectorXY(position)

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = VectorXY(normal)