class Matrix:
    def __init__(self, values: Iterable[float]):
        self._values = list(values)

    def __iter__(self):
        return iter(self._values)

    def __add__(self, other):
        is_scalar = isinstance(other, (float, int))
        if is_scalar:
            return Matrix(v + other for v in self._values)
        else:
            return Matrix(
                v1 + v2 for v1, v2 in zip(self, other)
            )

    def __sub__(self, other):
        is_scalar = isinstance(other, (float, int))
        if is_scalar:
            return Matrix(v - other for v in self._values)
        else:
            return Matrix(
                v1 - v2 for v1, v2 in zip(self, other)
            )

    def __mul__(self, other):
    is_scalar = isinstance(other, (float, int))
    if is_scalar:
        return Matrix(v * other for v in self._values)
    else:
        return Matrix(
            v1 - v2 for v1, v2 in zip(self, other)
        )
