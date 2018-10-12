from typing import Sequence
import collections

class ColorRGB(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        self._values = values

    @property
    def r(self) -> float:
        return self._values[0]

    @r.setter
    def r(self, r: float):
        self._values[0] = r

    @property
    def g(self) -> float:
        return self._values[1]

    @g.setter
    def g(self, g: float):
        self._values[1] = g

    @property
    def b(self) -> float:
        return self._values[2]

    @b.setter
    def b(self, b: float):
        self._values[2] = b

    def __iter__(self):
        return iter(self._values)

    def __eq__(self, other):
        return list(self) == list(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, value: float):
        self._values[index] = value

    def __str__(self):
        return " ".join(
            str(v for v in self._values)
        )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"r={self.r}, g={self.g}, b={self.b}"
            f")>"
        )