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
        self.powersource_name = "none"
        self.nominal_voltage = 0
        self.max_current = 0
        self.resistivity = 0
        self.wire_material_type = "Cu"
        self.wire_thickness = 1.0
        self.damage_flag = 0
        self.points = NotImplemented
        self.min_height = 0
        self.segment_length = 0
        self.wires_type = 1
        self.wire_offset = 0
        self.visible = True
        self.parallel_name = "none"


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
