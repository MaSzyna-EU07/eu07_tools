import abc

from eu07_tools.utils.structures import ColorRGB, VectorXYZ, Vertex3D


def create_submodel(type, name):
    if type == "Mesh":
        return T3DMeshSubmodel(name)
    elif type == "FreeSpotLight":
        return T3DFreeSpotLightSubmodel(name)
    elif type == "Stars":
        return T3DStarsSubmodel(name)
    
    raise ValueError(f"Bad T3D submodel type: {type}")


def create_include(path):
    return T3DInclude(path)


class T3DDatablock(abc.ABC):
    def __init__(self):
        self.datablock_type = ""


class T3DInclude(T3DDatablock):
    """ Included file representation """
    def __init__(self, path):
        self.datablock_type = "include"
        self.path = path


class T3DSubmodel(T3DDatablock):
    """ Base class for T3D submodels """
    def __init__(self, name):
        self.datablock_type = "submodel"
        self.parent_name = "none"
        self.name = name
        self.anim = "false"
        self._diffuse = ColorRGB((255, 255, 255))
        self.selfillum = 0
        self.type = ""
        self.max_distance = 1000
        self.min_distance = 0
        self.transform = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ]

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, diffuse):
        self._ambient = ColorRGB(diffuse)



class T3DMeshSubmodel(T3DSubmodel):
    """ T3D Mesh submodel representation """
    def __init__(self, name):
        super().__init__(name)   
        self.type = "Mesh"
        self._ambient = ColorRGB((255, 255, 255)) 
        self._specular = ColorRGB((255, 255, 255))
        self.wire = False
        self.wire_size = 1.0
        self.opacity = 100.0
        self.map = "none"
        self._triangles = []

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, ambient):
        self._ambient = ColorRGB(ambient)

    @property
    def specular(self) -> ColorRGB:
        return self._specular

    @specular.setter
    def specular(self, specular):
        self._specular = ColorRGB(specular)

    @property
    def num_verts(self):
        return len(self._triangles) * 3

    def add_triangle(self, vertices, smooth=0):
        """ Add new triangle with specified vertices and smooth mask """
        self._triangles.append(
            T3DTriangle(vertices, smooth)
        )

    def remove_triangle(self, triangle):
        """ Remove specified triangle from mesh """
        self._triangles.remove(triangle)

    @property
    def triangles(self):
        yield from iter(self._triangles)


class T3DTriangle:
    """ Representation of triangle in T3D Mesh submodel """
    def __init__(self, vertices, smooth=0):
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth = -1 if any(
            vertex.has_normal for vertex in self.vertices
        ) else smooth


class T3DFreeSpotLightSubmodel(T3DSubmodel):
    """ T3D FreeSpotLight submodel representation """
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
    """ T3D Stars submodel representation """
    def __init__(self, name):
        super().__init__(name)
        self.type = "Stars"
        self._stars = []

    def add_star(self, position, color):
        """ Add new star with specified position and color """
        self._stars.append(
            T3DStar(position, color)
        )

    def remove_star(self, star):
        """ Remove specified star from submodel """
        self._stars.remove(star)

    @property
    def stars(self):
        """ Return list of stars """
        return tuple(self._stars)

    @property
    def num_verts(self) -> int:
        return len(self._stars)


class T3DStar:
    def __init__(self, position, color):
        self._position = VectorXYZ(position)
        self._color = ColorRGB(color)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = VectorXYZ(position)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)