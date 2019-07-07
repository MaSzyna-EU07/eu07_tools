from . import SCNNode
from eu07_tools.utils import Vertex3D, FactorySequence, ColorRGB

class SCNNodeTriangles(SCNNode):
    def __init__(self, name):
        super().__init__(name)
        self.typename = "node:triangles"
        self.vertices = FactorySequence(Vertex3D, [
            Vertex3D((0, 0, 0, 0, 0, 0, 0, 0)),
            Vertex3D((0, 0, 0, 0, 0, 0, 0, 0)),
            Vertex3D((0, 0, 0, 0, 0, 0, 0, 0)),
        ])
        self.map = "none"
        self.material = None

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