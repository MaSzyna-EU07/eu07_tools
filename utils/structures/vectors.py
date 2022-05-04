from __future__ import annotations
from typing import Iterable, Callable, Iterator
import collections
import operator
import math


class BaseCollection:
    def __init__(self, values: Iterable[float]):
        self._values = list(values)

    def __contains__(self, item: float) -> bool:
        return item in self._values

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __getitem__(self, index: int) -> float:
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__len__())

            return self.__class__(self._values[start:stop:step])

        return self._values[index]

    def __setitem__(self, index: int, item: float):
        self._values[index] = item

    def __add__(self, other) -> BaseVector:
        return self._math_helper(operator.add, other)

    def __sub__(self, other) -> BaseVector:
        return self._math_helper(operator.sub, other)

    def __mul__(self, other) -> BaseVector:
        return self._math_helper(operator.mul, other)

    def __truediv__(self, other) -> BaseVector:
        return self._math_helper(operator.truediv, other)

    def __iadd__(self, other):
        self._values = list(self + other)
        return self

    def __eq__(self, other) -> bool:
        return self._values == other._values

    def __neg__(self):
        return self._math_helper(operator.mul, -1)

    def _math_helper(self, operator, other):
        if isinstance(other, (int, float)):
            return self.__class__((operator(v, other) for v in self._values))
        else:
            return self.__class__(
                (operator(v1, v2) for v1, v2 in zip(self._values, other))
            )

    def __repr__(self) -> str:
        values = ", ".join(str(v) for v in self._values)
        return f"<{self.__class__.__name__}({values})>"


class BaseVector(BaseCollection):
    @property
    def magnitude(self):
        return math.sqrt(sum(value ** 2 for value in self._values))

    @property
    def length(self):
        return self.magnitude

    @property
    def length_squared(self):
        return self.magnitude ** 2

    @property
    def normalized(self):
        if self.magnitude == 0:
            return self

        return self / self.magnitude

    def normalize(self):
        self._values = list(self.normalized)

    def dot(self, other):
        return sum(map(operator.mul, self, other))

    def is_negative(self, other):
        return self.dot(other) < -0.99

    def compare_equality(self, other, threshold=0.00001):
        vec = self - other
        return all(abs(x) < threshold for x in vec)

    def zero(self):
        self._values = [0 for value in self._values]


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

    def swizzled(self):
        return VectorXYZ((-self._values[0], self._values[2], self._values[1]))

    def cross(self, other):
        #TODO: Move up, make it possible to execute on 4 and 2dim vectors
        return self.__class__((
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0]
        ))


class VectorXYZW(VectorXYZ):
    @property
    def w(self):
        return self._values[3]

    @w.setter
    def w(self, w):
        self._values[3] = w


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


class ColorRGB(BaseCollection):
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


class ColorRGBA(ColorRGB):
    @property
    def a(self):
        return self._values[3]

    @a.setter
    def a(self, a):
        self._values[3] = a