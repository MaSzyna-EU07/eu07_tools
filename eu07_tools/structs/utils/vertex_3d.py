import collections
from typing import Iterable

from .vectors import VectorXYZ, VectorUV


class Vertex3D(collections.abc.Iterable):
    def __init__(self, values: Iterable[float]):
        values = list(values)
        num_values = len(values)

        if num_values in (5, 8):
            self._position = VectorXYZ(values[:3])
            self._normal = (
                VectorXYZ(values[3:6]) if num_values == 8 
                else VectorXYZ((0, 0, 0))
            )
            self._mapping = VectorUV(values[-2:])
        else:
            raise ValueError(
                f"Vertex3D constructor needs 5 or 8 values, {num_values} given"
            )

    @property
    def position(self) -> VectorXYZ:
        return self._position

    @position.setter
    def position(self, position):
        self._position = VectorXYZ(position)

    @property
    def normal(self) -> VectorXYZ:
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = VectorXYZ(normal)

    @property
    def mapping(self) -> VectorUV:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        self._mapping = VectorUV(mapping)

    @property
    def has_normal(self) -> bool:
        return self._normal != VectorXYZ((0, 0, 0))

    def __iter__(self):
        normal = self._normal if self.has_normal else []
        return iter((*self._position, *normal, *self._mapping))

    def __str__(self):
        return " ".join(str(v) for v in iter(self))

    def __repr__(self):
        values = ", ".join(str(v) for v in iter(self))
        return f"<{self.__class__.__name__}({values})>"