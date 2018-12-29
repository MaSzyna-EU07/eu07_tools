from eu07_tools.utils.structures import Vertex3D, ColorRGB

class SCNNode:
    def __init__(self, name):
        self.typename = ""
        self.name = ""
        self.max_distance = -1
        self.min_distance = 0


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
