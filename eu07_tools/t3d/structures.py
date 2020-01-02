import abc

from eu07_tools.utils.structures import ColorRGB, VectorXYZ, Vertex3D, FactorySequence


def create_submodel(type, name):
    """ Create named T3D submodel instance
    
    :param type: Typename of submodel - "Mesh", "FreeSpotLight" or "Stars"
    :type type: str
    :param name: Name of submodel

    :raises: `ValueError` if invalid type is given

    :return: Submodel instance of given type
    :rtype: :class:`t3d.Submodel`
    """
    type_l = type.lower()
    if type_l == "mesh":
        return MeshSubmodel(name)
    elif type_l == "freespotlight":
        return FreeSpotLightSubmodel(name)
    elif type_l == "stars":
        return StarsSubmodel(name)
    
    raise ValueError(f"Bad T3D submodel type: {type}")


def create_include(path, parameters):
    """ Create instance of T3D Include.

    :param path: Relative path to included file
    :type path: str
    :param parameters: Parameters list
    :type parameters: `List[str]` 

    :returns: Include object
    :rtype: :class:`t3d.Include`
    """
    return Include(path, parameters)


class Element(abc.ABC):
    """ Base abstract class for T3D elements (includes, submodels)

    :ivar element_type: Type name of element - can be "submodel" or "include"
    :type element_type: str
    """
    def __init__(self):
        """ Constructor method
        """
        self.element_type = ""


class Include(Element):
    """ Class representing include directive in T3D model.

    :ivar path: Relative path to included file
    :type path: str
    :ivar parameters: Parameters list
    :type parameters: `List[str]`  
    """
    def __init__(self, path, parameters=None):
        self.element_type = "include"
        self.path = path
        self.parameters = [] if parameters is None else list(parameters)


class Submodel(Element):
    """ Base class for submodels. Defines common attributes for subclasses.

    :ivar type: Submodel type name - can be "Mesh", "FreeSpotLight", "Stars". This value is read-only.
    :type type: `str`
    :ivar name: Name of submodel
    :type name: `str`
    :ivar parent_name: Parent name, defaults to "none"
    :type parent_name: `str`
    :ivar anim: Animation type, defaults to "false"
    :type anim: `str`
    :ivar diffuse_color: RGB diffuse color, values in range <0;255>, defaults to (255, 255, 255)
    :type diffuse_color: :class:`utils.ColorRGB` 
    :ivar selfillum: SelfIllum parameter, value in range <0;1.25>, defaults to 0
    :type selfillum: `float`
    :ivar max_distance: Maximum rendering distance in meters, defaults to 1000
    :type max_distance: `float`
    :ivar max_distance: Minimum rendering distance in meters, defaults to 0
    :type max_distance: `float`
    :ivar transform: Transform matrix as list of 16 floats, defaults to identity matrix.
    :type transform: `List[float]`
    """
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


class MeshSubmodel(Submodel):
    """ Mesh submodel class, inherits attributes from :class:`t3d.Submodel` and defines 
    attributes specific for it's type

    :ivar ambient_color: RGB ambient color, values in range <0;255>, defaults to (255, 255, 255)
    :type ambient_color: :class:`utils.ColorRGB`
    :ivar specular_color: RGB specular color, values in range <0;255>, defaults to (255, 255, 255)
    :type specular_color: :class:`utils.ColorRGB` 
    :ivar wire: Wireframe display state, defaults to False
    :type wire: `bool`
    :ivar wire_size: Wire thickness in wireframe display mode, defaults to 1.0
    :type wire_size: `float`
    :ivar opacity: Opacity level, value in range <0;1>, defaults to 1.0
    :type opacity: `float`
    :ivar map: Texture path or replacableskin id, defaults to "none"
    :type map: `str`
    :ivar triangles: Mutable collection of :class:`t3d.MeshTriangle` objects, by default it's empty
    :type triangles: :class:`utils.FactorySequence[t3d.MeshTriangle]`
    :ivar num_verts: Number of vertices in all triangles, defaults to 0. This value is read-only.
    :type num_verts: `int`
    """
    def __init__(self, name):
        super().__init__(name)   
        self.type = "Mesh"
        self._ambient_color = ColorRGB((255, 255, 255)) 
        self._specular_color = ColorRGB((255, 255, 255))
        self.wire = False
        self.wire_size = 1.0
        self.opacity = 1.0
        self.map = "none"
        self.triangles = FactorySequence(MeshTriangle)

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


class MeshTriangle:
    """ Class representing triangle in mesh submodel
    
    :ivar vertices: Tuple of 3 vertices
    :type vertives: `Tuple[utils.Vertex3D]`
    :ivar smooth: Smooth mask, -1 if vertices has explicit normal vectors
    :type smooth: `int`
    """
    def __init__(self, vertices, smooth=0):
        """ Constructor method

        :param vertices: Iterable of 3 vertices data
        :type vertices: `Iterable[Iterable[float]]`
        :param smooth: Smooth mask, -1 if vertices has explicit normal vectors
        :type smooth: `int`
        """
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth = -1 if any(
            vertex.has_normal for vertex in self.vertices
        ) else smooth


class FreeSpotLightSubmodel(Submodel):
    """ FreeSpotLight submodel class, inherits attributes from :class:`t3d.Submodel` and defines 
    attributes specific for it's type

    :ivar near_atten_start: Near attentuation start, defaults to 40.0
    :type near_atten_start: `float`
    :ivar near_atten_end: Near attentuation end, defaults to 0.0
    :type near_atten_end: `float` 
    :ivar use_near_atten: Near attentuation start usage state, defaults to False
    :type use_near_atten: `bool`
    :ivar far_atten_decay_type: Far attentuation decay type. Can be 0, 1, 2, defaults to 1
    :type far_atten_decay_type: `int`
    :ivar far_decay_radius: Far decay radius, defaults to 45.0
    :type far_decay_radius: `float`
    :ivar falloff_angle: Faloff angle, defaults to 45.0
    :type falloff_angle: `float`
    :ivar hotspot_angle: Hotspot angle, defaults to 45.0
    :type hotspot_angle: `float`
    """
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


class StarsSubmodel(Submodel):
    """ FreeSpotLight submodel class, inherits attributes from :class:`t3d.Submodel` and defines 
    attributes specific for it's type

    :ivar stars: Mutable collection of :class:`t3d.StarsLight` objects, by default it's empty
    :type stars: :class:`utils.FactorySequence[t3d.StarsLight]`
    :ivar num_verts: Number of light points, defaults to 0. This value is read-only.
    :type num_verts: `int`
    """
    def __init__(self, name):
        super().__init__(name)
        self.type = "Stars"
        self.stars = FactorySequence(StarsLight)

    @property
    def num_verts(self):
        return len(self.stars)


class StarsLight:
    """ Class representing light point in stars submodel
    
    :ivar location: Location of light point.
    :type vertives: :class:`utils.VectorXYZ`
    :ivar bin_color: BGR color of light as integer.
    :type bin_color: `int`
    :ivar rgb_color: RGB color of light.
    :type rgb_color: :class:`utils.ColorRGB`
    """
    def __init__(self, location, color):
        """ Constructor method
    
        :param location: Location of light point.
        :type vertives: `Iterable[float]`
        :param color: BGR color as integer or RGB color as 3-element sequence.
        :type bin_color: `Union[int, Sequence[float]]`
        """
        self._location = VectorXYZ(location)
        if isinstance(color, (int, float)):
            self.bin_color = int(color)
        else:
            self.rgb_color = color

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = VectorXYZ(location)

    @property
    def rgb_color(self):
        return ColorRGB((
            (self.bin_color & 0xff),
            ((self.bin_color >> 8) & 0xff),
            ((self.bin_color >> 16) & 0xff)
        ))

    @rgb_color.setter
    def rgb_color(self, rgb_color):
        self.bin_color = (
            (int(rgb_color[0])) | (int(rgb_color[1]) << 8) | (int(rgb_color[2]) << 16)
        )
