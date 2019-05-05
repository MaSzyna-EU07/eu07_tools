from eu07_tools.utils.structures import VectorXYZ, ColorRGB

from .nodes import *


class SCNAtmo:
    def __init__(self):
        self.typename = "atmo"
        self._sky_color = ColorRGB((1, 1, 1))
        self.fog_start = 1700
        self.fog_end = 2000
        self._fog_color = ColorRGB((153, 179, 204))
        self.overcast = 0.1


class SCNCamera:
    def __init__(self):
        self.typename = "camera"
        self._position = VectorXYZ((0, 0, 0))
        self._rotation = VectorXYZ((0, 0, 0))
        self.index = -1

class SCNFirstInit:
    def __init__(self):
        self.typename = "firstinit"


class SCNInclude:
    def __init__(self):
        self.typename = "include"
        self.path = ""
        self._parameters = []

    def append_parameter_value(self, value):
        self._parameters.append(value)

    def set_parameter_value(self, param_id, value):
        self._parameters[param_id-1] = value

    def get_parameter_value(self, param_id):
        return self._parameters[param_id - 1]


class SCNLua:
    def __init__(self):
        self.typename = "lua"
        self.path = ""


class SCNOrigin(VectorXYZ):
    def __init__(self, values):
        super().__init__(values)
        self.typename = "origin"

class SCNEndOrigin:
    def __init__(self):
        self.typename = "endorigin"


class SCNRotate(VectorXYZ):
    def __init__(self, values):
        super().__init__(values)
        self.typename = "rotate"


class SCNSky:
    def __init__(self):
        self.typename = "sky"
        self.model_path = ""


class SCNTime:
    def __init__(self):
        self.typename = "time"
        self.initial_time = ""
        self.sunset_time = ""
        self.sunrise_time = ""


class SCNTrainset:
    def __init__(self):
        self.typename = "trainset"
        self.timetable_path = "rozklad"
        self.track_name = "none"
        self.offset = 0
        self.velocity = 0

class SCNEndTrainset:
    def __init__(self):
        self.typename = "endtrainset"
