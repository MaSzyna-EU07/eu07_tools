from typing import Iterable, Callable, Sequence
import collections
import operator

class BaseVector(collections.abc.MutableSequence):
    def __init__(self, values: Iterable[float]):
        self._values = values

    def __iter__(self):
        return iter(self._values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, item: float):
        self._values[index] = item

    def __delitem__(self, item: float):
        pass

    def __add__(self, other):
        return self._math_helper(operator.add, other)

    def __sub__(self, other):
       return self._math_helper(operator.sub, other)

    def __mul__(self, other):
        return self._math_helper(operator.mul, other)

    def __div__(self, other):
        return self._math_helper(operator.truediv, other)

    def __eq__(self, other):
        return list(self) == list(other)
        
    def _math_helper(self, operator: Callable[float, float], other):
        if isinstance(other, (int, float)):
            return (operator(v, other) for v in iter(self))
        else:
            return (operator(a, b) for a, b in zip(self, other))

    def __str__(self) -> str:
        return " ".join(str(v) for v in self._values)


class VectorXYZ(BaseVector):
    def __init__(self, values):
        super().__init__(values)

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


class VectorUV(BaseVector):
    @property
    def u(self) -> float:
        return self._values[1]

    @u.setter
    def u(self, u: float):
        self._values[1] = u

    @property
    def v(self) -> float:
        return self._values[2]

    @v.setter
    def v(self, v: float):
        self._values[2] = v


class ColorRGB(BaseVector):
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