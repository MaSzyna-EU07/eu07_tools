from . import SCNNode
from eu07_tools.utils import ColorRGB, FactorySequence, VectorXYZ

class SCNNodeLines(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:lines"
        self._color = ColorRGB((0, 0, 0))
        self.thickness = 1.0
        self.points = FactorySequence(VectorXYZ)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)

class SCNNodeLineStrip(SCNNodeLines):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:line_strip"

class SCNNodeLineLoop(SCNNodeLines):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:line_loop"