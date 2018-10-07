from __future__ import annotations
import collections
from typing import Any, Iterable, Sequence


class ColorRGB(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        self.r, self.g, self.b = values

    def __iter__(self):
        return iter((self.r, self.g, self.b))

    def __eq__(self, other):
        return (
            self.r == other.r and
            self.g == other.g and
            self.b == other.b
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.r} {self.g} {self.b}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"r={self.r}, g={self.g}, b={self.b}"
            f")>"
        )


class Vector4(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        self.x, self.y, self.z, self.v = values

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.v))

    def __eq__(self, other):
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z and
            self.v == other.v
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"x={self.x}, y={self.y}, z={self.z}, v={self.v}"
            f")>"
        )


class Vector3(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        self.x, self.y, self.z = values

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"x={self.x}, y={self.y}, z={self.z}"
            f")>"
        )

    def __eq__(self, other) -> bool:
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


class Vector2(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        self.x, self.y = values

    def __iter__(self) -> Iterable[float]:
        return iter((self.x, self.y))

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"x={self.x}, y={self.y}"
            f")>"
        )
    
    def __eq__(self, other) -> bool:
        return (
            self.x == other.x and
            self.y == other.y
        )


class Bezier3D:
    pass


class Vertex3D(collections.abc.Iterable):
    def __init__(self, values: Sequence[float]):
        num_values = len(values)
        if num_values in (5, 8):
            self._position = Vector3(values[:3])
            self._normal = (
                Vector3(values[3:6]) if num_values == 8 
                else Vector3((0, 0, 0))
            )
            self._mapping = Vector2(values[-2:])
        else:
            raise ValueError(
                f"Vertex3D constructor needs 5 or 8 values, {num_values} given"
            )

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = Vector3(*position)

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, normal):
        self._normal = Vector3(*normal)

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        self._mapping = Vector2(*mapping)

    def __iter__(self):
        normal = [] if self._normal == Vector3((0, 0, 0)) else self._normal
        return iter((*self._position, *normal, *self._mapping))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"position={repr(self._position)}, "
            f"normal={repr(self._normal)}, "
            f"mapping={repr(self._mapping)},"
            f")>"   
        )
