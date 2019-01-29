from eu07_tools.utils.structures import Vertex3D, ColorRGB, VectorXYZ

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
        self.base_path = ""
        self.map = ""
        self.mmd_path = ""
        self.track_name = "none"
        self.offset = 0
        self.driver_type = "nobody"
        self.coupling = "3"
        self.velocity = 0
        self.load_count = 0
        self.load_type = ""
        self.destination = ""


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


class SCNNodeLines(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:lines"
        self._color = ColorRGB((0, 0, 0))
        self.thickness = 1.0
        self.points = []

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)

    def add_point(self, position):
        self.points.append(VectorXYZ(position))

class SCNNodeLineStrip(SCNNodeLines):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:line_strip"

class SCNNodeLineLoop(SCNNodeLines):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:line_loop"

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
        self.light_states = []

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

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

class SCNNodeTraction(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:traction"
        self.powersource_name = "none"
        self.nominal_voltage = 0
        self.max_current = 0
        self.resistivity = 0
        self.wire_material_type = "Cu"
        self.wire_thickness = 1.0
        self.damage_flag = 0
        self.points = []
        self.min_height = 0
        self.segment_length = 0
        self.wires_type = 1
        self.wire_offset = 0
        self.visible = True
        self.parallel_name = "none"

class SCNNodeTractionPowerSource(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:tractionpowersource"
        self._location = VectorXYZ((0, 0, 0))
        self.nominal_voltage = 0
        self.voltage_frequency = 0
        self.internal_resistance = 0
        self.max_output_current = 0
        self.fast_fuse_timeout = 0
        self.fast_fuse_repetition = 0
        self.slow_fuse_timeout = 0
        self.recuperation = False
        self.section = False

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

class SCNNodeTrack(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track"
        self.length = 0
        self.width = 1.435
        self.friction = 0.2
        self.sound_distance = 0
        self.damage_flag = 0
        self.environment = "flat"
        self.visible = True
        self.map1 = ""
        self.tex_length = 4
        self.map2 = ""
        self._p1 = VectorXYZ((0, 0, 0))
        self._cv1 = VectorXYZ((0, 0, 0))
        self._cv2 = VectorXYZ((0, 0, 0))
        self._p1 = VectorXYZ((0, 0, 0))
        self.radius = 0
        self.optional_parameters = {}

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, location):
        self._p1 = VectorXYZ(location)

    @property
    def cv1(self):
        return self._cv1

    @cv1.setter
    def cv1(self, location):
        self._cv1 = VectorXYZ(location)

    @property
    def cv2(self):
        return self._cv2

    @cv2.setter
    def cv2(self, location):
        self._cv2 = VectorXYZ(location)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, location):
        self._p2 = VectorXYZ(location)

class SCNNodeTrackNormal(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:normal"

class SCNNodeTrackRoad(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:road"

class SCNNodeTrackRiver(SCNNodeTrack):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:track:river"

class SCNNodeTrackSwitch(SCNNodeTrack):
    pass


class SCNNodeTrackCross(SCNNodeTrack):
    pass


class SCNNodeTriangles(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:triangles"
        self.vertices = []
        self.map = "none"
        self.material = None

    def add_vertex(self, vertex):
        self.vertices.append(Vertex3D(vertex))

class SCNNodeTriangleStrip(SCNNodeTriangles):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:triangle_strip"


class SCNNodeTriangleFan(SCNNodeTriangles):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:triangle_fan"


class SCNTrianglesMaterial:
    def __init__(self, ambient, diffuse, specular):
        self._ambient = ColorRGB(ambient)
        self._diffuse = ColorRGB(diffuse)
        self._specular = ColorRGB(specular)

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, color):
        self._ambient = ColorRGB(color)

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, color):
        self._diffuse = ColorRGB(color)

    @property
    def specular(self):
        return self._specular

    @specular.setter
    def specular(self, color):
        self._specular = ColorRGB(color)

    