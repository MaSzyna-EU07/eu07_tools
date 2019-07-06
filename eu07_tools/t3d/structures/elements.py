import abc

from eu07_tools.utils.structures import ColorRGB, VectorXYZ, Vertex3D, IndexedFactoryContainer


def create_submodel(type, name):
    """ 
    Factory function for creating submodel instances.
    
    :param type: typename of submodel (*Mesh*, *FreeSpotLight*, *Stars*)
    :type type: str
    :param name: name of submodel
    :type name: str

    :raises ValueError: in case of invalid submodel type

    :returns: Concrete submodel representation depending on *type* parameter
    :rtype: :class:`T3DSubmodel` subclasses
    """
    type_l = type.lower()
    if type_l == "mesh":
        return T3DMeshSubmodel(name)
    elif type_l == "freespotlight":
        return T3DFreeSpotLightSubmodel(name)
    elif type_l == "stars":
        return T3DStarsSubmodel(name)
    
    raise ValueError(f"Bad T3D submodel type: {type}")


def create_include(path):
    """
    Factory function for creating include objects.

    :param path: relative filepath to included file
    :type path: str

    :rtype: :class:`T3DInclude`
    """
    return T3DInclude(path)


class T3DElement(abc.ABC):
    """
    Base class for all T3D model elements (submodels and includes)

    :ivar element_type: typename of element (*submodel*, *include*), used to distinguish includes and submodels
    :type element_type: str
    """
    def __init__(self):
        self.element_type = ""


class T3DInclude(T3DElement):
    """ 
    A subclass of :class:`T3DElement`, represents included file.
    
    :ivar path: relative filepath to included file
    :type path: str
    """
    def __init__(self, path):
        self.element_type = "include"
        self.path = path


class T3DSubmodel(T3DElement):
    """ 
    Base class for concrete submodel representations, subclass of :class:`T3DElement`.

    :ivar name: name of submodel
    :type name: str
    :ivar parent_name: name of parent submodel
    :type parent_name: str
    :ivar anim: animation type
    :type anim: str
    :ivar diffuse: diffuse color
    :type diffuse: :class:`ColorRGB`http://eksploratorzy.com.pl/viewtopic.php?f=21&t=6076&start=60
    :ivar selfillum: light emission threshold
    :type selfillum: float, <-1.25; 1.25>
    :ivar max_distance: maximal rendering radius. In case of unlimited range, this value should be equal -1.
    :type max_distance: float
    :ivar min_distance: minimal rendering radius, >=0
    :type min_distance: float
    :ivar transform: transformation matrix as a 16-element :class:`list` 
    :type transform: `List[float]`
    """
    def __init__(self, name):
        self.element_type = "submodel"
        self.submodel_type = ""
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
    """ 
    Representation of *Mesh* submodel, subclass of :class:`T3DSubmodel`

    :ivar ambient: ambient color
    :type ambient: :class:`ColorRGB`
    :ivar specular: specular color
    :type specular: :class:`ColorRGB`
    :ivar wire: wireframe display mode flag
    :type wire: bool
    :ivar wire_size: line thickness in wireframe mode
    :type wire_size: float
    :ivar opacity: opacity level 
    :type opacity: float <0;100>
    :ivar map: texture path or replaceable skin identifier (*-1*, *-2*, *-3*, *-4*). *none* by default.
    :type map: str
    :ivar num_verts: number of vertices in all triangles, >=0
    :type num_verts: `int`
    :ivar triangles: list of triangles
    :type map: `List[T3DTriangle]`
    """
    def __init__(self, name):
        super().__init__(name)   
        self.submodel_type = "Mesh"
        self._ambient_color = ColorRGB((255, 255, 255)) 
        self._specular_color = ColorRGB((255, 255, 255))
        self.wire = False
        self.wire_size = 1.0
        self.opacity = 100.0
        self.map = "none"
        self.triangles = IndexedFactoryContainer(T3DTriangle)

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


class T3DTriangle:
    """
    3D triangle class.

    :ivar vertices: tuple of vertices
    :type vertices: `Tuple[Vertex3D]`
    :ivar smooth: smooth bitflag - should be -1 if there are explicit normal vectors
    :type smooth: `int`, optional, default: 0
    """
    def __init__(self, vertices, smooth=0):
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth = -1 if any(
            vertex.has_normal for vertex in self.vertices
        ) else smooth


class T3DFreeSpotLightSubmodel(T3DSubmodel):
    """ 
    Representation of *FreeSpotLight* submodel, subclass of :class:`T3DSubmodel`

    :ivar near_atten_start:
    :type near_atten_start: `float`
    "ivar near_atten_end:
    :type near_atten_end: `float`
    :ivar use_near_atten:
    :type use_near_atten:
    :ivar far_atten_decay_type:
    :type far_atten_decay_type: `int`
    :ivar far_decay_radius:
    :type far_decay_radius: `float`
    :ivar falloff_angle:
    :type falloff_angle: `float`
    :ivar hotspot_angle:
    :type hotspot_angle: `float`
    """
    def __init__(self, name):
        super().__init__(name)
        self.submodel_type = "FreeSpotLight"
        self.near_atten_start = 40.0
        self.near_atten_end = 0.0
        self.use_near_atten = False
        self.far_atten_decay_type = 1
        self.far_decay_radius = 45.0
        self.falloff_angle = 45.0
        self.hotspot_angle = 45.0


class T3DStarsSubmodel(T3DSubmodel):
    """
    Representation of *Stars* submodel, subclass of :class:`T3DSubmodel`

    :ivar num_verts: number of stars
    :type num_verts: `int`
    :ivar stars: list of stars
    :type stars: `List[T3DStar]`
    """
    def __init__(self, name):
        super().__init__(name)
        self.submodel_type = "Stars"
        self.stars = IndexedFactoryContainer(T3DStar)

    @property
    def num_verts(self):
        return len(self.stars)


class T3DStar:
    """
    Light point class for Stars submodel

    :ivar location: location of star
    :type location: `VectorXYZ`
    :ivar color: RGB color of star
    :type color: `ColorRGB`
    """

    def __init__(self, location, color):
        self._location = VectorXYZ(location)
        self._color = ColorRGB(color)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = ColorRGB(color)