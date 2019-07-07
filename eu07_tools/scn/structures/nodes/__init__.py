from eu07_tools.utils.structures import Vertex3D, ColorRGB, VectorXYZ, FactorySequence

class SCNNode:
    def __init__(self, name):
        self.typename = ""
        self.name = ""
        self.max_distance = -1
        self.min_distance = 0


class SCNNodeDynamic(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:dynamic"
        self.base_path = "none"
        self.map = "none"
        self.mmd_path = "none"
        self.track_name = "none"
        self.offset = 0
        self.driver_type = "nobody"
        self.coupling = "3"
        self.velocity = 0
        self.load_count = 0
        self.load_type = "none"
        self.destination = "none"


class SCNNodeEventlauncher(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:eventlauncher"
        self._location = VectorXYZ((0, 0, 0))
        self.radius = -1
        self.key = "none"
        self.delta_time = 0
        self.first_event_name = "none"
        self.second_event_name = "none"
        self.memcell_name = "none"
        self.check_mask = 0

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)


class SCNNodeMemcell(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self._location = VectorXYZ((0, 0, 0))
        self.values = ["none", 0, 0]
        self.track_name = "none"

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)


class SCNNodeModel(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:model"
        self._location = VectorXYZ((0, 0, 0))
        self.rotation_y = 0
        self.path = ""
        self.map = ""
        self.lights = FactorySequence(ModelLight)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

class ModelLight:
    def __init__(self, state, color):
        self.state = state
        self._color = ColorRGB(color)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)


class SCNNodeSound(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:sound"
        self._location = VectorXYZ((0, 0, 0))
        self.path = ""

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)







    