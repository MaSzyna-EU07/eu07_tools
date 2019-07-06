from eu07_tools.utils import IndexedFactoryContainer, Vertex3D

class E3DStruct:
    def __init__(self):
        self.submodels = IndexedFactoryContainer(E3DSubmodel)
        self.names = IndexedFactoryContainer(str)
        self.matrices = IndexedFactoryContainer(list)
        self.vertices = IndexedFactoryContainer(Vertex3D)
        self.materials = IndexedFactoryContainer(str, ["none?"])


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
        self.ambient_color = []
        self.diffuse_color = []
        self.specular_color = []
        self.emission_color =[]
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