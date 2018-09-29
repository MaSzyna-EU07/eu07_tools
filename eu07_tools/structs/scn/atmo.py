from typing import Iterable

from eu07_tools.structs.utils import ColorRGB


class SCNAtmo:
    def __init__(self, sky_color: Iterable[float], fog_start: float, 
                       fog_end: float, fog_color: Iterable[float], 
                       overcast: float):
        self.fog_start = fog_start
        self.fog_end = fog_end
        self.overcast = overcast

        self._fog_color = fog_color
        self._sky_color = sky_color

    @property
    def fog_color(self) -> ColorRGB:
        return self._fog_color

    @fog_color.setter
    def fog_color(self, fog_color: Iterable[float]):
        self._fog_color = ColorRGB(fog_color)

    @property
    def sky_color(self) -> ColorRGB:
        return self._sky_color

    @sky_color.setter
    def sky_color(self, sky_color: Iterable[float]):
        self._sky_color = ColorRGB(sky_color)