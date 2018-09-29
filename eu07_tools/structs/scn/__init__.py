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


# TODO: More generic case?
class SCNConfig:
    def __init__(self, content):
        self._conf_dict = {}

    def __getitem__(self, key: str) -> Any:
        return self._conf_dict[key]

    def __setitem__(self, key: str, value: Any):
        self._conf_dict[key] = value


class SCNLight:
    def __init__(self, location, ambient, diffuse, specular):
        self._location = Vector3(location)
        self._ambient = ColorRGB(ambient)
        self._diffuse = ColorRGB(diffuse)
        self._specular = ColorRGB(specular)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = Vector3(location)

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, ambient):
        self._ambient = ColorRGB(ambient)

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, diffuse):
        self._diffuse = ColorRGB(diffuse)

    @property
    def specular(self):
        return self._specular

    @specular.setter
    def specular(self, specular):
        self._specular = ColorRGB(specular)


class SCNSky:
    def __init__(self, model_name: str):
        self.model_name = model_name


class SCNTime:
    def __init__(self, start_time: str, sunset_time: str, sunrise_time: str):
        self.start_time = datetime.time()
        self.sunset_time = sunset_time
        self.sunrise_time = sunrise_time

class SCNTrainset:
    def __init__(self, name, track_name, offset, vehicles=[]):
        pass