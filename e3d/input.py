import struct

import eu07_tools
from .common import VERTEX_SIZE, CHUNK_HEADER_SIZE, MATRIX_SIZE, SUBMODEL_SIZE


def load(file):
    inp = E3DInput(file)
    return inp.load()


class E3DInput:
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
        self._scanner.read_bytes(CHUNK_HEADER_SIZE)

        self.model = eu07_tools.e3d.create_model()

        while not self._scanner.is_empty:
            chunk_id, chunk_size = self._read_header()

            chunk_read = self._chunk_readers.get(chunk_id)

            data_size = chunk_size - CHUNK_HEADER_SIZE
            chunk_read(data_size)

        return self.model

    def _read_header(self):
        chunk_id = self._scanner.read_str(4)
        chunk_size = self._scanner.read_int()

        return chunk_id, chunk_size

    def _read_SUB0(self, data_size):
        NUM_SUBMODELS = data_size // SUBMODEL_SIZE

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
        num_verts = data_size // VERTEX_SIZE

        for _ in range(num_verts):
            vertex = [self._scanner.read_float() for _ in range(8)]
            self.model.vertices.new(vertex)

    def _read_TRA0(self, data_size):
        num_matrices = data_size // MATRIX_SIZE

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