from eu07_tools.utils import FactoryContainer, Vertex3D, ColorRGBA

class E3DStruct:
    def __init__(self):
        self.submodels = FactoryContainer(E3DSubmodel)
        self.names = FactoryContainer(str)
        self.matrices = FactoryContainer(list)
        self.vertices = FactoryContainer(Vertex3D)
        self.materials = FactoryContainer(str, ["none"])


class E3DSubmodel:
    def __init__(self):
        # TODO: More accurate initial values
        # TODO: RGBAColor for colors (properties)
        self.next_id = -1
        self.first_child_id = -1
        self.submodel_type_id = -1
        self.name_id = -1
        self.anim_id = -1
        self.first_vertex_id = -1
        self.material_id = -1

        self.flags = 0
        self.transform_id = -1
        self.num_verts = 0
        self.light_level_treshold = 0
        self.light_emission_treshold = 0
        self._ambient_color = ColorRGBA((1, 1, 1, 1))
        self._diffuse_color = ColorRGBA((1, 1, 1, 1))
        self._specular_color = ColorRGBA((1, 1, 1, 1))
        self._emission_color = ColorRGBA((1, 1, 1, 1))
        self.wire_size = 0
        self.max_distance = 1000
        self.min_distance = 0
        self.near_atten_start = 0
        self.near_atten_end = 0
        self.use_near_atten = False
        self.far_atten_decay_tape = 0
        self.far_decay_radius = 0
        self.cos_falloff_angle = 0
        self.cos_hotspot_angle = 0
        self.cos_view_angle = 0

    @property
    def ambient_color(self):
        return self._ambient_color

    @ambient_color.setter
    def ambient_color(self, ambient_color):
        self._ambient_color = ColorRGBA(ambient_color)

    @property
    def diffuse_color(self):
        return self._diffuse_color

    @diffuse_color.setter
    def diffuse_color(self, diffuse_color):
        self._diffuse_color = diffuse_color

    @property
    def specular_color(self):
        return self._specular_color

    @specular_color.setter
    def specular_color(self, specular_color):
        self._specular_color = specular_color