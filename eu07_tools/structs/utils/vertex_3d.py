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

    def __getitem__(self, index: int) -> float:
        return tuple(self)[index]

    def __setitem__(self, index: int, value: float):
        raise NotImplementedError()

    def __str__(self):
        return " ".join(str(v) for v in iter(self))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"position={repr(self._position)}, "
            f"normal={repr(self._normal)}, "
            f"mapping={repr(self._mapping)},"
            f")>"   
        )