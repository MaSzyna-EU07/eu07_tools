from __future__ import annotations
from typing import Iterable, Callable, Iterator
import collections
import operator
import math

class BaseVector(collections.abc.MutableSequence):
    def __init__(self, values: Iterable[float]):
        self._values = list(values)

    def __contains__(self, item: float) -> bool:
        return item in self._values
    
    def insert(self, index: int, item: object):
        pass

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, item: float):
        self._values[index] = item

    def __delitem__(self, item: float):
        pass

    def __add__(self, other) -> BaseVector:
        return self._math_helper(operator.add, other)

    def __sub__(self, other) -> BaseVector:
       return self._math_helper(operator.sub, other)

    def __mul__(self, other) -> BaseVector:
        return self._math_helper(operator.mul, other)

    def __div__(self, other) -> BaseVector:
        return self._math_helper(operator.truediv, other)

    def __iadd__(self, other) -> BaseVector:
        self._values = list(self + other)
        return self

    def __eq__(self, other) -> bool:
        return list(self) == list(other)

    def __neg__(self) -> BaseVector:
        return self._math_helper(operator.mul, -1)
        
    def _math_helper(self, operator: Callable[float, float], other) -> BaseVector:
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
    def x(self) -> float:
        return self._values[0]

    @x.setter
    def x(self, x: float):
        self._values[0] = x

    @property
    def y(self) -> float:
        return self._values[1]

    @y.setter
    def y(self, y: float):
        self._values[1] = y

    @property
    def z(self) -> float:
        return self._values[2]

    @z.setter
    def z(self, z: float):
        self._values[2] = z


class VectorXY(BaseVector):
    @property
    def x(self) -> float:
        return self._values[0]

    @x.setter
    def x(self, x: float):
        self._values[0] = x

    @property
    def y(self) -> float:
        return self._values[1]

    @y.setter
    def y(self, y: float):
        self._values[1] = y


class VectorUV(BaseVector):
    @property
    def u(self) -> float:
        return self._values[0]

    @u.setter
    def u(self, u: float):
        self._values[0] = u

    @property
    def v(self) -> float:
        return self._values[1]

    @v.setter
    def v(self, v: float):
        self._values[1] = v


class ColorRGB(BaseVector):
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