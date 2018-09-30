from typing import Iterable, List

from eu07_tools.structs.utils import Vector3, ColorRGB, Vertex3D

class SCNNode:
    """ Base class for nodes """
    def __init__(self, name: str):
        self.max_distance: float = -1.0
        self.min_distance: float = 0
        self.name: str = name


class SCNNodeEventLauncher(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._position: Vector3 = Vector3((0, 0, 0))
        self.radius: float = -1.0
        self.key = "none?"
        self.delta_time: float = 0

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = position


class SCNNodeLines(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._color: ColorRGB = ColorRGB((255, 255, 255))
        self.thickness: float = 1.0
        self._vertices_positions = []

    def add_vertex_position(self, position: Iterable[float]):
        self._vertices_positions.append(Vector3(position))

    def get_vertex_position(self, index: int) -> Vector3:
        return self._vertices_positions[index]


class SCNNodeLineStrip(SCNNodeLines): pass


class SCNNodeLineLoop(SCNNodeLines): pass


class SCNNodeMemcell(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._position: Vector3 = Vector3((0, 0, 0))
        self.values: List[str, float, float] = []
        self.linked_node_name: str = "none"

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = position


class SCNNodeModel(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._position: Vector3 = Vector3((0, 0, 0))
        self.rotation_y: float = 0
        self.file_path: str = ""
        self.replacableskin: str = ""
        self.light_states = []

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = position


class SCNNodeSound(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._position: Vector3 = Vector3((0, 0, 0))
        self.file_path: str = ""

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = position


class SCNNodeTractionPowerSource(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._position: Vector3 = Vector3((0, 0, 0))
        self.nominal_voltage: float = 0.0
        self.voltage_frequency: float = 0.0
        self.internal_resistance: float = 0.2
        self.max_output_current: float = 0.0
        self.fast_fuse_timeout: float = 1.0
        self.fast_fuse_repetition: int = 3
        self.slow_fuse_timeout: float = 0.0
        self.recuperation: bool = True
        self.section: bool = True

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Iterable[float]):
        self._position = position

class SCNNodeTraction(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.power_supply_name: str = "none"
        self.nominal_voltage: float = 0.0
        self.max_current: float = 0.0
        self.resistivity: float = 0.0
        self.material: str = "Cu"
        self.thickness: float = 1.0
        self.damage_flag: int = 0
        self.height_difference: float = 0.0
        self.segment_length: float = 0.0
        self.num_wires: int = 2
        self.wire_offset: float = 0.0
        self.visible: bool = True
        self.parallel_name = "none"
        self._p1: Vector3 = Vector3((0, 0, 0))
        self._p2: Vector3 = Vector3((0, 0, 0))
        self._p3: Vector3 = Vector3((0, 0, 0))
        self._p4: Vector3 = Vector3((0, 0, 0))
    
    @property
    def p1(self) -> Vector3:
        return self._p1

    @p1.setter
    def p1(self, p1: Iterable[float]):
        self._p1 = Vector3(p1)

    @property
    def p2(self) -> Vector3:
        return self._p2

    @p2.setter
    def p2(self, p2: Iterable[float]):
        self._p2 = Vector3(p2)

    @property
    def p3(self) -> Vector3:
        return self._p3

    @p3.setter
    def p3(self, p3: Iterable[float]):
        self._p3 = Vector3(p3)

    @property
    def p4(self) -> Vector3:
        return self._p4

    @p4.setter
    def p4(self, p4: Iterable[float]):
        self._p4 = Vector3(p4)


class SCNNodeTriangles(SCNNode):
    class Material:
        def __init__(self, ambient: Iterable[float] = [255, 255, 255], 
                           diffuse: Iterable[float] = [255, 255, 255], 
                           specular: Iterable[float] = [255, 255, 255]):
            self._ambient: ColorRGB = ColorRGB((ambient))
            self._diffuse: ColorRGB = ColorRGB((diffuse))
            self._specular: ColorRGB = ColorRGB((specular))

        @property
        def ambient(self) -> ColorRGB:
            return self._ambient

        @ambient.setter
        def ambient(self, ambient: Iterable[float]):
            self._ambient = ColorRGB(ambient)

        @property
        def diffuse(self) -> ColorRGB:
            return self._diffuse

        @diffuse.setter
        def diffuse(self, diffuse: Iterable[float]):
            self._diffuse = ColorRGB(diffuse)

        @property
        def specular(self) -> ColorRGB:
            return self._specular

        @specular.setter
        def specular(self, specular: Iterable[float]):
            self._specular = ColorRGB(specular)

    def __init__(self, name: str):
        super().__init__(name)
        self.material = self.Material()
        self.texture_path = "none"
        self._vertices = []

    def add_vertex(self, values: Iterable[float]):
        self._vertices.append(Vertex3D(values))

    def get_vertex(self, index: int) -> Vertex3D:
        return self._vertices[index]

    def remove_vertex(self, vertex: Vertex3D):
        self._vertices.remove(vertex)

class SCNNodeTriangleStrip(SCNNodeTriangles): pass

class SCNNodeTriangleFan(SCNNodeTriangles): pass