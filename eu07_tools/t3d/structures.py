import abc

from eu07_tools.utils.structures import ColorRGB, VectorXYZ, Vertex3D, FactorySequence


def create_submodel(type, name):
    type_l = type.lower()
    if type_l == "mesh":
        return T3DMeshSubmodel(name)
    elif type_l == "freespotlight":
        return T3DFreeSpotLightSubmodel(name)
    elif type_l == "stars":
        return T3DStarsSubmodel(name)
    
    raise ValueError(f"Bad T3D submodel type: {type}")


def create_include(path):
    return T3DInclude(path)


class T3DElement(abc.ABC):
    def __init__(self):
        self.element_type = ""


class T3DInclude(T3DElement):
    def __init__(self, path):
        self.element_type = "include"
        self.path = path


class T3DSubmodel(T3DElement):
    def __init__(self, name):
        self.element_type = "submodel"
        self.type = ""
        self.name = name
        self.parent_name = "none"
        self.anim = "false"
        self._diffuse_color = ColorRGB((255, 255, 255))
        self.selfillum = 0
        self.max_distance = 1000
        self.min_distance = 0
        self.transform = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ]

    @property
    def diffuse_color(self):
        return self._diffuse_color

    @diffuse_color.setter
    def diffuse_color(self, diffuse_color):
        self._diffuse_color = ColorRGB(diffuse_color)



class T3DMeshSubmodel(T3DSubmodel):
    def __init__(self, name):
        super().__init__(name)   
        self.type = "Mesh"
        self._ambient_color = ColorRGB((255, 255, 255)) 
        self._specular_color = ColorRGB((255, 255, 255))
        self.wire = False
        self.wire_size = 1.0
        self.opacity = 100.0
        self.map = "none"
        self.triangles = TrianglesFactorySequence(T3DTriangle)

    @property
    def ambient_color(self):
        return self._ambient_color

    @ambient_color.setter
    def ambient_color(self, ambient_color):
        self._ambient_color = ColorRGB(ambient_color)

    @property
    def specular_color(self) -> ColorRGB:
        return self._specular_color

    @specular_color.setter
    def specular_color(self, specular_color):
        self._specular_color = ColorRGB(specular_color)

    @property
    def num_verts(self):
        return len(self.triangles) * 3


class TrianglesFactorySequence(FactorySequence):
    def __init__(self, cls, initial_list=None):
        super().__init__(cls, initial_list)

    def new(self, vertices, smooth):
        triangle = self.cls(vertices, smooth)
        self._items.append(triangle)
        return triangle


class T3DTriangle:
    def __init__(self, vertices, smooth=0):
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth = -1 if any(
            vertex.has_normal for vertex in self.vertices
        ) else smooth


class T3DFreeSpotLightSubmodel(T3DSubmodel):
    def __init__(self, name):
        super().__init__(name)
        self.type = "FreeSpotLight"
        self.near_atten_start = 40.0
        self.near_atten_end = 0.0
        self.use_near_atten = False
        self.far_atten_decay_type = 1
        self.far_decay_radius = 45.0
        self.falloff_angle = 45.0
        self.hotspot_angle = 45.0


class T3DStarsSubmodel(T3DSubmodel):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Stars"
        self.stars = FactorySequence(T3DStar)

    @property
    def num_verts(self):
        return len(self.stars)


class T3DStar:
    def __init__(self, location, bin_color):
        self._location = VectorXYZ(location)
        self.bin_color = bin_color

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

    @property
    def rgb_color(self):
        return ColorRGB((
            (self.bin_color & 0xff) / 255.0,
            ((self.bin_color >> 8) & 0xff) / 255.0,
            ((self.bin_color >> 16) & 0xff) / 255.0
        ))
