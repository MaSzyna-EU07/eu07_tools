from eu07_tools.utils.structures import VectorXYZ, ColorRGB, Vertex3D, FactorySequence


class Atmo:
    def __init__(self):
        self.type = "atmo"
        self._sky_color = ColorRGB((255, 255, 255))
        self.fog_start = 1700
        self.fog_end = 2000
        self._fog_color = ColorRGB((153, 179, 204))
        self.overcast = 0.1


class Camera:
    def __init__(self):
        self.type = "camera"
        self._location = VectorXYZ((0, 0, 0))
        self._rotation = VectorXYZ((0, 0, 0))
        self.index = -1

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = VectorXYZ(rotation)


class Config:
    def __init__(self):
        pass


class Description:
    def __init__(self):
        pass


class Event:
    def __init__(self, name):
        self.name = "name"
        self.type = "event"
        self.subtype = "multiple"
        self.delay = 0
        self.node_name = "none"


class FirstInit:
    def __init__(self):
        self.type = "firstinit"


class Include:
    def __init__(self):
        self.type = "include"
        self.path = ""
        self.parameters = []


class Light:
    def __init__(self):
        pass


class Lua:
    def __init__(self):
        self.type = "lua"
        self.path = ""


class Origin:
    def __init__(self):
        self.type = "origin"
        self._vector = VectorXYZ((0, 0, 0))
    
    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, vector):
        self._vector = vector

class EndOrigin:
    def __init__(self):
        self.type = "endorigin"


class Rotate:
    def __init__(self, values):
        self.type = "rotate"
        self._vector = VectorXYZ((0, 0, 0))
    
    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, vector):
        self._vector = vector


class Sky:
    def __init__(self):
        self.type = "sky"
        self.model_path = ""


class Time:
    def __init__(self):
        self.type = "time"
        self.initial_time = ""
        self.sunset_time = ""
        self.sunrise_time = ""


class Trainset:
    def __init__(self):
        self.type = "trainset"
        self.timetable_path = "rozklad"
        self.track_name = "none"
        self.offset = 0
        self.velocity = 0
        self.assignment = {}

class EndTrainset:
    def __init__(self):
        self.type = "endtrainset"