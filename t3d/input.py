from collections.abc import Iterator
import eu07_tools.t3d
from eu07_tools.utils import TextScanner
from eu07_tools.utils.structures.mesh_geometry import MeshGeometry


def load_from_path(filepath)
    if filepath.endswith(".e3d")
        inp = E3DInput
        mode = "rb"
        encoding = None
    elif filepath.endswith(".t3d")
        inp = T3DInput
        mode = "r"
        encoding = "latin-1"
    else:
        raise ValueError("Bad model path! Extension should be *.t3d or *.e3d")

    with open(filepath, mode, encoding=encoding) as file:
        return inp.load(file)

def load(file):
    return T3DInput(file).load()


class T3DInput:
    def __init__(self, file):
        self._scanner = TextScanner.from_file(file)
        
    def load(self):
        while True:
            token = self._scanner.read_string().lower().rstrip(":")

            if token == "":
                return
            elif token == "parent":
                parent_name = self._scanner.read_string()
                try:
                    yield self._load_submodel(parent_name)
                except ValueError as e:
                    raise ValueError(f"Bad T3D syntax in line: {self._scanner.line_number}")
            elif token == "include":
                path, *parameters = self._scanner.read_strings_before("end")
                yield eu07_tools.t3d.create_include(path, parameters)

    def _load_submodel(self, parent_name):
        type_ = self._read_property()
        name = self._read_property()

        submodel = eu07_tools.t3d.create_submodel(type_, name)

        submodel.parent_name = parent_name
        submodel.anim = self._read_property()

        if submodel.type == "Mesh":
            submodel.ambient_color = self._read_property()
            submodel.diffuse_color = self._read_property()
            submodel.specular_color = self._read_property()
            submodel.selfillum = self._read_property()
            submodel.wire = self._read_property()
            submodel.wire_size = self._read_property()
            submodel.opacity = self._read_property()
            submodel.map = self._read_property()

        elif submodel.type == "FreeSpotLight":
            submodel.diffuse_color = self._read_property()
            submodel.selfillum = self._read_property()
            submodel.near_atten_start = self._read_property()
            submodel.near_atten_end = self._read_property()
            submodel.use_near_atten = self._read_property()
            submodel.far_atten_decay_type = self._read_property()
            submodel.far_decay_radius = self._read_property()
            submodel.falloff_angle = self._read_property()
            submodel.hotspot_angle = self._read_property()

        elif submodel.type == "Stars":
            submodel.diffuse_color = self._read_property()
            submodel.selfillum = self._read_property()

        submodel.max_distance = self._read_property()
        submodel.min_distance = self._read_property()
        submodel.transform = self._read_property()

        if submodel.type in "Stars Mesh":
            self._load_geometry(submodel)

        return submodel

    def _load_geometry(self, submodel):
        token = self._scanner.read_string().lower()
        # TODO: Too much if-type, get rid of this

        if submodel.type == "Mesh":
            geo = submodel.geometry = MeshGeometry()

        if "numindices" in token:
            geo.type = MeshGeometry.Type.INDEXED
            num_indices = self._scanner.read_int()

            for i in range(num_indices):
                geo.indices.append(self._scanner.read_int())

            num_verts = self._read_property()
            for i in range(num_verts):
                vertex = geo.vertices.new(self._scanner.read_floats(12))

        elif "numverts" in token:
            num_total_verts = self._scanner.read_int()

            num_loaded_verts = 0
            MAX_UNIT_SIZE = 3

            if num_total_verts % MAX_UNIT_SIZE == 0:
                LAST_UNIT_SIZE = MAX_UNIT_SIZE
            else:
                LAST_UNIT_SIZE = num_total_verts % MAX_UNIT_SIZE

            while num_loaded_verts < num_total_verts:
                is_last_unit = (num_loaded_verts + MAX_UNIT_SIZE >= num_total_verts)
                unit_size = LAST_UNIT_SIZE if is_last_unit else MAX_UNIT_SIZE
                num_loaded_verts += unit_size

                unit_flag = self._scanner.read_int()

                vertex_size = 8 if unit_flag == -1 else 5
                vertices = [self._scanner.read_floats(vertex_size) for _ in range(unit_size)]

                if submodel.type == "Mesh":
                    geo.triangles.new(vertices, unit_flag)
                elif submodel.type == "Stars":
                    for vertex in vertices:
                        submodel.stars.new(vertex[:3], vertex[3])


    def _read_property(self):
        propname = self._scanner.read_string().lower().rstrip(":")

        if propname in ("ambient", "diffuse", "specular"):
            value = self._scanner.read_floats(3)

        elif propname in ("transform",):
            value = self._scanner.read_floats(16)

        elif propname in ("usenearatten", "wire"):
            value = (self._scanner.read_string() == "true")

        elif propname in ("selfillum",):
            token = self._scanner.read_string()
            if token == "false":
                value = -1.0
            elif token == "true":
                value = 2.0
            else:
                value = float(token)

        elif propname in ("numverts", "farattendecaytype"):
            value = self._scanner.read_int()

        elif propname in ("parent", "name", "map", "anim", "type"):
            value = self._scanner.read_string()

        elif propname == "opacity":
            value = self._scanner.read_float()
            if value > 1:
                value = value / 100

        else:
            value = self._scanner.read_float()

        return value


class E3DInput:
    VERTEX_SIZE = 32
    MATRIX_SIZE = 64
    CHUNK_HEADER_SIZE = 8
    SUBMODEL_SIZE = 256

    TYPEID_TO_TYPENAME = {
        4: "Mesh",
        256: "Mesh",
        257: "FreeSpotLight",
        258: "Stars"
    }

    ANIMID_TO_ANIMTYPENAME = {
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

    def __init__(self, file):
        self._chunk_readers = {
            "SUB0": self._read_SUB0,
            "VNT0": self._read_VNT0,
            "TEX0": self._read_TEX0,
            "NAM0": self._read_NAM0,
            "TRA0": self._read_TRA0,
            "IDX0": self._read_IDX0,
        }

        self._scanner = eu07_tools.utils.BinaryScanner(file)

    def load(self):
        self._scanner.read_bytes(self.CHUNK_HEADER_SIZE)

        self.model = eu07_tools.e3d.create_model()

        while not self._scanner.is_empty:
            chunk_id, chunk_size = self._read_header()

            chunk_read = self._chunk_readers.get(chunk_id)

            data_size = chunk_size - self.CHUNK_HEADER_SIZE
            chunk_read(data_size)

        return self.model

    def _read_header(self):
        chunk_id = self._scanner.read_str(4)
        chunk_size = self._scanner.read_int()

        return chunk_id, chunk_size

    def _read_SUB0(self, data_size):
        NUM_SUBMODELS = data_size // self.SUBMODEL_SIZE

        for _ in range(NUM_SUBMODELS):
            submodel = self.model.submodels.new()

            submodel.next_submodel_id = self._scanner.read_int()
            submodel.first_child_id = self._scanner.read_int()
            submodel.type_id = self._scanner.read_int()
            submodel.name_id = self._scanner.read_int()
            submodel.anim_id = self._scanner.read_int()
            submodel.flags = self._scanner.read_int()
            submodel.matrix_id = self._scanner.read_int()
            submodel.num_verts = self._scanner.read_int()
            submodel.first_vertex_id = self._scanner.read_int()
            submodel.material_id = self._scanner.read_int()
            submodel.visibility_light_treshold = self._scanner.read_float()
            submodel.selfillum = self._scanner.read_float()
            submodel.ambient_color = self._scanner.read_floats(4)
            submodel.diffuse_color = self._scanner.read_floats(4)
            submodel.specular_color = self._scanner.read_floats(4)
            submodel.emission_color = self._scanner.read_floats(4)
            submodel.wire_size = self._scanner.read_float()
            submodel.max_distance = self._scanner.read_float()
            submodel.min_distance = self._scanner.read_float()
            submodel.near_atten_start = self._scanner.read_float()
            submodel.near_atten_end = self._scanner.read_float()
            submodel.use_near_atten = self._scanner.read_bool()
            submodel.far_atten_decay_type = self._scanner.read_int()
            submodel.far_decay_radius = self._scanner.read_float()
            submodel.cos_falloff_angle = self._scanner.read_float()
            submodel.cos_hotspot_angle = self._scanner.read_float()
            submodel.cos_view_angle = self._scanner.read_float()
            submodel.num_indices = self._scanner.read_int()
            submodel.first_vertex_id = self._scanner.read_int()

            # skip pad bytes
            self._scanner.read_bytes(92)

    def _read_IDX0(self, data_size):
        pass

    def _read_VNT0(self, data_size):
        num_verts = data_size // self.VERTEX_SIZE

        for _ in range(num_verts):
            vertex = [self._scanner.read_float() for _ in range(8)]
            self.model.vertices.new(vertex)

    def _read_TRA0(self, data_size):
        num_matrices = data_size // self.MATRIX_SIZE

        for _ in range(num_matrices):
            matrix = [self._scanner.read_float() for _ in range(16)]
            self.model.matrices.new(matrix)

    def _read_TEX0(self, data_size):
        self._read_zero_separated_values(data_size, self.model.material_names)

    def _read_NAM0(self, data_size):
        self._read_zero_separated_values(data_size, self.model.names)

    def _read_zero_separated_values(self, data_size, collection):
        data = self._scanner.read_str(data_size)
        values = data.strip("\x00").split("\x00")

        for value in values:
            collection.new(value)

