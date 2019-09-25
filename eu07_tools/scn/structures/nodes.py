from eu07_tools.utils.structures import VectorXYZ, ColorRGB, Vertex3D, FactorySequence

class Node:
    def __init__(self, name):
        self.type = ""
        self.name = name
        self.max_distance = -1
        self.min_distance = 0


class NodeDynamic(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:dynamic"
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


class NodeEventlauncher(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:eventlauncher"
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


class NodeLines(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:lines"
        self.subtype = "normal"
        self._color = ColorRGB((0, 0, 0))
        self.thickness = 1.0
        self.points = FactorySequence(VectorXYZ)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)


class NodeMemcell(Node):
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


class NodeModel(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:model"
        self._location = VectorXYZ((0, 0, 0))
        self.rotation_y = 0
        self.path = ""
        self.map = ""
        self.light_states = []
        self.light_colors = []

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

class NodeSound(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:sound"
        self._location = VectorXYZ((0, 0, 0))
        self.path = ""

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)


class NodeTrack(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:track"
        self._subtype = "normal"
        self.length = 0
        self.width = 1.435
        self.friction = 0.15
        self.sound_distance = 20
        self.quality_flag = 0
        self.damage_flag = 0
        self.environment = "flat"
        self.is_visible = True
        self.map1 = "none"
        self.map2 = "none"
        self.mapping_length = 4
        self.geometry_param1 = 0
        self.geometry_param2 = 0
        self.geometry_param3 = 0
        self._p1 = VectorXYZ((0, 0, 0))
        self.p1_roll = 0
        self._cv1 = VectorXYZ((0, 0, 0))
        self._p2 = VectorXYZ((0, 0, 0))
        self._cv2 = VectorXYZ((0, 0, 0))
        self.p2_roll = 0
        self._p3 = None
        self._cv3 = None
        self.p3_roll = 0
        self._p4 = None
        self._cv4 = None
        self.p4_roll = 0
        self.radius1 = 0
        self.radius2 = 0

        self.velocity = 0
        self.event0 = "none"
        self.event1 = "none"
        self.event2 = "none"
        self.eventall0 = "none"
        self.eventall1 = "none"
        self.eventall2 = "none"
        self.isolated = "none"
        self.overhead = -1
        self.angle1 = 0
        self.angle2 = 0
        self.fouling1 = "none"
        self.fouling2 = "none"
        self.vradius = 0
        self.trackbed = "none"
        self.railprofile = "none"

    @property
    def is_junction(self):
        return self._subtype in ("switch", "cross", "tributary")

    @property
    def subtype(self):
        return self._subtype

    @subtype.setter
    def subtype(self, subtype):
        self._subtype = subtype

        if subtype in "normal road river turn table":
            self._p3 = None
            self._cv3 = None
            self._cv4 = None
            self._p4 = None
        else:
            self._p3 = VectorXYZ((0, 0, 0))
            self._cv3 = VectorXYZ((0, 0, 0))
            self._cv4 = VectorXYZ((0, 0, 0))
            self._p4 = VectorXYZ((0, 0, 0))

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        self._p1 = VectorXYZ(p1)

    @property
    def cv1(self):
        return self._cv1

    @cv1.setter
    def cv1(self, cv1):
        self._cv1 = VectorXYZ(cv1)

    @property
    def cv2(self):
        return self._cv2

    @cv2.setter
    def cv2(self, cv2):
        self._cv2 = VectorXYZ(cv2)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        self._p2 = VectorXYZ(p2)

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, p3):
        self._p3 = VectorXYZ(p3)

    @property
    def cv3(self):
        return self._cv3

    @cv3.setter
    def cv3(self, cv3):
        self._cv3 = VectorXYZ(cv3)

    @property
    def cv4(self):
        return self._cv4

    @cv4.setter
    def cv4(self, cv4):
        self._cv4 = VectorXYZ(cv4)

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, p4):
        self._p4 = VectorXYZ(p4)


class NodeTraction(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:traction"
        self.powersource_name = "none"
        self.nominal_voltage = 0
        self.max_current = 0
        self.resistance = 0
        self.wire_material_type = "Cu"
        self.wire_thickness = 1.0
        self.damage_flag = 0
        self._p1 = VectorXYZ((0, 0, 0))
        self._p2 = VectorXYZ((0, 0, 0))
        self._p3 = VectorXYZ((0, 0, 0))
        self._p4 = VectorXYZ((0, 0, 0))
        self.min_height = 0
        self.segment_length = 0
        self.wires_type = 1
        self.wire_offset = 0
        self.is_visible = True
        self.parallel_name = "none"

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1):
        self._p1 = VectorXYZ(p1)

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2):
        self._p2 = VectorXYZ(p2)

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, p3):
        self._p3 = VectorXYZ(p3)

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, p4):
        self._p4 = VectorXYZ(p4)


class NodeTractionPowerSource(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:tractionpowersource"
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


class NodeTriangles(Node):
    def __init__(self, name):
        super().__init__(name)
        self.type = "node:triangles"
        self.subtype = "normal"
        self.vertices = FactorySequence(Vertex3D)
        self.map = "none"
        self.material = _TrianglesMaterial()

class _TrianglesMaterial:
    def __init__(self):
        self.is_used = False
        self._ambient = ColorRGB((255, 255, 255))
        self._diffuse = ColorRGB((255, 255, 255))
        self._specular = ColorRGB((255, 255, 255))

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, color):
        if color is None:
            self._ambient = None
        else:
            self._ambient = ColorRGB(color)

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, color):
        if color is None:
            self._diffuse = None
        else:
            self._diffuse = ColorRGB(color)

    @property
    def specular(self):
        return self._specular

    @specular.setter
    def specular(self, color):
        if color is None:
            self._specular = None
        else:
            self._specular = ColorRGB(color)
