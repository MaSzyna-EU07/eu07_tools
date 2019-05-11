from __future__ import annotations
from typing import Iterable, Callable, Iterator
import collections
import operator
import math

class BaseVector:
    def __init__(self, values: Iterable[float]):
        self._values = list(values)

    def __contains__(self, item: float) -> bool:
        return item in self._values

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, item: float):
        self._values[index] = item

    def __add__(self, other) -> BaseVector:
        return self._math_helper(operator.add, other)

    def __sub__(self, other) -> BaseVector:
       return self._math_helper(operator.sub, other)

    def __mul__(self, other) -> BaseVector:
        return self._math_helper(operator.mul, other)

    def __div__(self, other) -> BaseVector:
        return self._math_helper(operator.truediv, other)

    def __iadd__(self, other):
        self._values = list(self + other)
        return self

    def __eq__(self, other) -> bool:
        return list(self) == list(other)

    def __neg__(self):
        return self._math_helper(operator.mul, -1)
        
    def _math_helper(self, operator, other):
        if isinstance(other, (int, float)):
            return VectorXYZ((operator(v, other) for v in self._values))
        else:
            return VectorXYZ(
                (operator(v1, v2) for v1, v2 in zip(self._values, other))
            )

    def __repr__(self) -> str:
        values = ", ".join(str(v) for v in self._values)
        return f"<{self.__class__.__name__}({values})>"


class VectorXYZ(BaseVector):
    @property
    def x(self):
        return self._values[0]

    @x.setter
    def x(self, x):
        self._values[0] = x

    @property
    def y(self):
        return self._values[1]

    @y.setter
    def y(self, y):
        self._values[1] = y

    @property
    def z(self):
        return self._values[2]

    @z.setter
    def z(self, z):
        self._values[2] = z


class VectorXY(BaseVector):
    @property
    def x(self):
        return self._values[0]

    @x.setter
    def x(self, x):
        self._values[0] = x

    @property
    def y(self):
        return self._values[1]

    @y.setter
    def y(self, y):
        self._values[1] = y


class VectorUV(BaseVector):
    @property
    def u(self):
        return self._values[0]

    @u.setter
    def u(self, u):
        self._values[0] = u

    @property
    def v(self):
        return self._values[1]

    @v.setter
    def v(self, v):
        self._values[1] = v


class ColorRGB(BaseVector):
    @property
    def r(self):
        return self._values[0]

    @r.setter
    def r(self, r):
        self._values[0] = r

    @property
    def g(self):
        return self._values[1]

    @g.setter
    def g(self, g):
        self._values[1] = g

    @property
    def b(self):
        return self._values[2]

    @b.setter
    def b(self, b):
        self._values[2] = b