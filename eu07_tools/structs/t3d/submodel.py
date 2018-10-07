from __future__ import annotations
import abc
from typing import Iterable, Sequence

from eu07_tools.structs.utils import ColorRGB


class T3DSubmodel(abc.ABC):
    def __init__(self, name: str):
        self.parent_name = "none"
        self.name: str = name
        self.type = ""
        self.anim: str = "false" # Enum here?
        self._diffuse: ColorRGB = ColorRGB((255, 255, 255))
        self.self_illum: float = 1.0
        self.max_distance: float = 1000.0
        self.min_distance: float = 0.0
        self.transform: Sequence[Sequence[float]]= [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
        
    @property
    def diffuse(self) -> ColorRGB:
        return self._diffuse

    @diffuse.setter
    def diffuse(self, diffuse: Iterable[float]):
        self._diffuse = ColorRGB(diffuse)


    def __repr__(self) -> str:
        return "<" + self.__class__.__name__ + f": {self.name}>"

