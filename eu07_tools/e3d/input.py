import struct

from eu07_tools.utils import BinaryScanner
from .structures import E3DModel


def load(file):
    inp = E3DInput(file)
    return inp.load()
    
_VERTEX_SIZE = 8 * 4
_TRA0_MATRIX_SIZE = 16 * 4
_HEADER_SIZE = 8
_SUBMODEL_SIZE = 256

class E3DInput:
    def __init__(self, file):
        self._chunk_readers = {
            "SUB0": self._read_SUB0,
            "VNT0": self._read_VNT0,
            "TEX0": self._read_TEX0,
            "NAM0": self._read_NAM0,
            "TRA0": self._read_TRA0,
        }

        self._scanner = BinaryScanner(file)

    def load(self):
        self._scanner.read_bytes(_HEADER_SIZE)

        self.model = E3DModel()

        while not self._scanner.is_empty:
            chunk_id, chunk_size = self._read_header()

            chunk_read = self._chunk_readers.get(chunk_id)

            chunk_read(chunk_size)
    
        return self.model

    def _read_header(self):
        chunk_id = self._scanner.read_str(4)
        chunk_size = self._scanner.read_int()

        return chunk_id, chunk_size


    def _read_SUB0(self, chunk_size):
        NUM_SUBMODELS = chunk_size // _SUBMODEL_SIZE

        for _ in range(NUM_SUBMODELS):
            submodel = self.model.submodels.new()

            submodel.next_id = self._scanner.read_int()
            submodel.first_child_id = self._scanner.read_int()
            submodel.submodel_type_id = self._scanner.read_int()
            submodel.name_id = self._scanner.read_int()
            submodel.anim_id = self._scanner.read_int()
            submodel.flags = self._scanner.read_int()
            submodel.transform_id = self._scanner.read_int()
            submodel.num_verts = self._scanner.read_int()
            submodel.first_vertex_id = self._scanner.read_int()
            submodel.material_id = self._scanner.read_int()
            submodel.visibility_light_treshold = self._scanner.read_float()
            submodel.selfillum = self._scanner.read_float()
            submodel.ambient_color = [self._scanner.read_float() for _ in range(4)]
            submodel.diffuse_color = [self._scanner.read_float() for _ in range(4)]
            submodel.specular_color = [self._scanner.read_float() for _ in range(4)]
            submodel.emission_color = [self._scanner.read_float() for _ in range(4)]
            submodel.wire_size = self._scanner.read_float()
            submodel.max_distance = self._scanner.read_float()
            submodel.min_distance = self._scanner.read_float()
            submodel.near_atten_start = self._scanner.read_float()
            submodel.near_atten_end = self._scanner.read_float()
            submodel.use_near_atten = self._scanner.read_float()
            submodel.far_atten_decay_type = self._scanner.read_float()
            submodel.far_decay_radius = self._scanner.read_float()
            submodel.cos_falloff_angle = self._scanner.read_float()
            submodel.cos_hotspot_angle = self._scanner.read_float()
            submodel.cos_view_angle = self._scanner.read_float()

            # skip pad bytes
            self._scanner.read_bytes(100)
            

    def _read_VNT0(self, chunk_size):
        num_verts = chunk_size // _VERTEX_SIZE

        for _ in range(num_verts):
            vertex = [self._scanner.read_float() for _ in range(8)]
            self.model.vertices.new(vertex)
                

    def _read_TRA0(self, chunk_size):
        num_matrices = chunk_size // _TRA0_MATRIX_SIZE

        for _ in range(num_matrices):
            matrix = [self._scanner.read_float() for _ in range(16)]
            self.model.matrices.new(matrix)

    def _read_TEX0(self, chunk_size):
        self._read_zero_separated_values(chunk_size, self.model.materials)

    def _read_NAM0(self, chunk_size):
        self._read_zero_separated_values(chunk_size, self.model.names)

    def _read_zero_separated_values(self, chunk_size, collection):
        data = self._scanner.read_str(chunk_size - 8)
        values = data.strip("\x00").split("\x00")

        for value in values:
            collection.new(value)



