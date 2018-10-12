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

    def __getitem__(self, index: int) -> float:
        return tuple(self)[index]

    def __setitem__(self, index: int, value: float):
        raise NotImplementedError()

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

    def __getitem__(self, index: int) -> float:
        return tuple(self)[index]

    def __setitem__(self, index: int, value: float):
        raise NotImplementedError()

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

    def __getitem__(self, index: int) -> float:
        return tuple(self)[index]

    def __setitem__(self, index: int, value: float):
        raise NotImplementedError()
    
    def __eq__(self, other) -> bool:
        return (
            self.x == other.x and
            self.y == other.y
        )