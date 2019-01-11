from .nodes import (
    SCNNode,
    SCNNodeTriangles,
    SCNNodeTriangleFan,
    SCNNodeTriangleStrip,
    SCNTrianglesMaterial
)

]


class SCNAtmo:
    def __init__(self):
        self.typename = "atmo"
        self._sky_color = ColorRGB(1, 1, 1)
        self.fog_start = 1700
        self.fog_end = 2000
        self._fog_color = ColorRGB(153, 179, 204)
        self.overcast = 0.1


class SCNCamera:
    def __init__(self):
        self.typename = "camera"
        self._position = VectorXYZ(0, 0, 0)
        self._rotation = VectorXYZ(0, 0, 0)
        self.index = -1