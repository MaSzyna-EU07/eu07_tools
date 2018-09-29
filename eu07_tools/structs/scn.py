class Scenery:
    def __init__(self):
        self.atmo = SCNAtmo()
        self.sky = SCNSky()
        self.config = {}
        self.cameras = []
        self.events = []
        self.paths = []


class SCNAtmo:
    def __init__(self, sky_color, fog_start, fog_end, fog_color, overcast):
        self.sky_color = sky_color
        self.fog_start = fog_start
        self.fog_end = fog_end
        self.fog_color = fog_color
        self.overcast = overcast


class SCNCamera:
    def __init__(self, position, rotation, index: int):
        self.position = position
        self.rotation = rotation
        self.index = index


class SCNEvent:
    pass


class SCNInclude:
    pass


class SCNLight:
    pass


class SCNLua:
    pass


class SCNNode:
    pass


class SCNNodeTriangles(SCNNode):
    pass


class SCNOrigin:
    def __init__(self, vector):
        self.vector = vector


class SCNRotate:
    def __init__(self, vector):
        self.vector = vector


class SCNSky:
    def __init__(self, model_name: str):
        self.model_name = model_name


class SCNTime:
    def __init__(self, time: str, sunset_time: str, sunrise_time: str):
        pass

class SCNTrainset:
    def __init__(self, name, track_name, offset, vehicles=[]):
        pass
