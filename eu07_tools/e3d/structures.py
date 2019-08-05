from eu07_tools.utils import FactorySequence, Vertex3D, ColorRGBA

def create_model(self):
    return Model()


class Model:
    def __init__(self):
        self.submodels = OwnedFactorySequence(Submodel, owner=self)
        self.names = FactorySequence(str)
        self.matrices = FactorySequence(list)
        self.vertices = FactorySequence(Vertex3D)
        self.material_names = FactorySequence(str, initial_list=[""])

class OwnedFactorySequence(FactorySequence):
    def __init__(self, cls, initial_list=None, owner=None):
        super().__init__(cls, initial_list)
        self.owner = owner

    def new(self, *args):
        instance = super().new(*args)
        instance.owner = self.owner

class Submodel:
    def __init__(self):
        # TODO: More accurate initial values
        self.owner = None

        self.next_submodel_id = -1
        self.first_child_id = -1
        self.submodel_type_id = -1
        self.name_id = -1
        self.anim_id = -1
        self.first_vertex_id = -1
        self.material_id = -1

        self.flags = 0
        self.matrix_id = 0
        self.num_verts = 0
        self.visibility_light_treshold = 0
        self.selfillum = 0
        self._ambient_color = ColorRGBA((1, 1, 1, 1))
        self._diffuse_color = ColorRGBA((1, 1, 1, 1))
        self._specular_color = ColorRGBA((1, 1, 1, 1))
        self._emission_color = ColorRGBA((1, 1, 1, 1))
        self.wire_size = 1
        self.max_distance = 1000
        self.min_distance = 0
        self.near_atten_start = 40
        self.near_atten_end = 0
        self.use_near_atten = False
        self.far_atten_decay_type = 0
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

    @property
    def name(self):
        return "none" if self.name_id == -1 else self.owner.names[self.name_id]

    @property
    def material_name(self):
        return "none" if self.name_id in (-1, 0) else self.owner.material_names[self.material_id]

    @property
    def transform(self):
        return None if self.matrix_id == -1 else self.owner.matrices[self.matrix_id]

    @property
    def first_child(self):
        return None if self.first_child_id == -1 else self.owner.submodels[self.first_child_id]

    @property
    def next_submodel(self):
        return None if self.next_submodel_id == -1 else self.owner.submodels[self.next_submodel_id]

    @property
    def children(self):
        current = self.first_child
        yield current
        while current.next_submodel is not None:
            yield current.next_submodel
            current = current.next_submodel


