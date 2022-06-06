from eu07_tools.utils import VectorXY, FactorySequence


class RailProfile:
    def __init__(self, name):
        self.name = name
        self.rail_points = FactorySequence(RailProfilePoint)
        self.blade_points = FactorySequence(RailProfilePoint)


class RailProfilePoint:
    def __init__(self, values):
        self._position = VectorXY(values[:2])
        self._normal = VectorXY(values[2:4])
        self.mapping = values[4]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = VectorXY(position)

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = VectorXY(normal)