from typing import Iterable

from eu07_tools.structs.utils import Vector3

class SCNCamera:
    def __init__(self, position: Iterable[float], 
                       rotation: Iterable[float], 
                       index: int):
        self.index = index

        self._position = position
        self._rotation = rotation

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = Vector3(position)

    @property
    def rotation(self) -> Vector3:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: Iterable[float]):
        self._rotation = Vector3(rotation)