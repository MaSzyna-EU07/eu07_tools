from typing import Iterable

from eu07_tools.structs.utils import Vector3, ColorRGB

class SCNNode:
    """ Base class for nodes """
    def __init__(self, name: str):
        self.max_distance: float = -1.0
        self.min_distance: float = 0
        self.name: str = name


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


class SCNNodeModel(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._location: Vector3 = Vector3((0, 0, 0))
        self.rotation_y: float = 0
        self.file_path: str = ""
        self.replacableskin: str = ""
        self.light_states = []

    @property
    def location(self) -> Vector3:
        return self._location

    @location.setter
    def location(self, location: Iterable[float]):
        self._location = location


class SCNNodeSound(SCNNode):
    def __init__(self, name: str):
        super().__init__(name)
        self._location: Vector3 = Vector3((0, 0, 0))
        self.file_path: str = ""

    @property
    def location(self) -> Vector3:
        return self._location

    @location.setter
    def location(self, location: Iterable[float]):
        self._location = location
    
