from __future__ import annotations
from typing import Iterable, Sequence

from .submodel import T3DSubmodel
from eu07_tools.structs.utils import ColorRGB, Vector3


class T3DStarsSubmodel(T3DSubmodel):
    def __init__(self, name: str):
        super().__init__(name)
        self.type_name = "Stars"
        self._stars: Sequence[T3DStar] = []

    def add_star(self, position: Iterable[float], color: Iterable[float]):
        """ Add new star with specified position and color """
        self._stars.append(
            T3DStar(position, color)
        )

    def remove_star(self, star: T3DStar):
        """ Remove specified star from submodel """
        self._stars.remove(star)

    def stars(self) -> Sequence[T3DStar]:
        """ Return list of stars """
        return tuple(self._stars)


class T3DStar:
    def __init__(self, position: Iterable[float], color: Iterable[float]):
        self._position = Vector3(position)
        self._color = ColorRGB(color)

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = Vector3(position)

    @property
    def color(self) -> ColorRGB:
        return self._color

    @color.setter
    def color(self, color: Iterable[float]):
        self._color = ColorRGB(color)