from eu07_tools.utils import FactorySequence, OwnedFactorySequence, Vertex3D, ColorRGBA

def create_model():
    return Model()


class Model:
    def __init__(self):
        self.submodels = OwnedFactorySequence(Submodel, owner=self)
        self.names = FactorySequence(str)
        self.matrices = FactorySequence(list)
        self.vertices = FactorySequence(Vertex3D)
        self.material_names = FactorySequence(str, initial_list=["none"])

_TYPEID_TO_TYPENAME = {
    4: "Mesh",
    256: "Mesh",
    257: "FreeSpotLight",
    258: "Stars"
}

_ANIMID_TO_ANIMTYPENAME = {
    -1: "true",
    0: "false",
    4: "seconds_jump",
    5: "minutes_jump",
    6: "hours_jump",
    7: "hours24_jump",
    8: "seconds",
    9: "minutes",
    10: "hours",
    11: "hours24",
    12: "billboard",
    13: "wind",
    14: "sky",
    256: "ik",
    257: "ik1",
    258: "ik2"
}

class Submodel:
    def __init__(self):
        # TODO: More accurate initial values
        self.owner = None

        self.next_submodel_id = -1
        self.first_child_id = -1
        self.type_id = 256
        self.name_id = -1
        self.anim_id = -1
        self.first_vertex_id = -1
        self.material_id = -1

        self.flags = 0
        self.matrix_id = 0
        self.num_verts = 0
        self.visibility_light_treshold = 0
        self.selfillum = -1
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
    def type(self):
        return _TYPEID_TO_TYPENAME[self.type_id]

    @property
    def anim(self):
        return _ANIMID_TO_ANIMTYPENAME.get(self.anim_id, "false")

    @property
    def name(self):
        return "none" if self.name_id == -1 else self.owner.names[self.name_id]

    @property
    def map(self):
        if self.material_id < 0:
            return str(self.material_id)
        elif self.material_id == 0:
            return "none"
        else:
            return self.owner.material_names[self.material_id]

    @property
    def transform(self):
        if self.matrix_id == -1:
            return [
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
            ]
        else: 
            return self.owner.matrices[self.matrix_id]

    @property
    def parent(self):
        for sm in self.owner.submodels:
            if self in sm.children:
                return sm

        return None

    @property
    def parent_name(self):
        if self.parent:
            return self.parent.name

        return "none"

    @property
    def first_child(self):
        return None if self.first_child_id == -1 else self.owner.submodels[self.first_child_id]

    @property
    def next_submodel(self):
        return None if self.next_submodel_id == -1 else self.owner.submodels[self.next_submodel_id]

    @property
    def vertices(self):
        return self.owner.vertices[
            self.first_vertex_id:
            self.first_vertex_id + self.num_verts
        ]

    @property
    def children(self):
        current = self.first_child
        while current is not None:
            yield current
            current = current.next_submodel

    @property
    def id(self):
        return self.owner.submodels.index(self)

    @property
    def has_geometry(self):
        return self.num_verts > 0


