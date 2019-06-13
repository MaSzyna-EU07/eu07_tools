import struct

from eu07_tools.utils import BinaryScanner

#TODO: Refactor magic numbers
def load(file):
    inp = E3DInput(file)
    return inp
    
_VERTEX_SIZE = 8 * 4
_TRA0_MATRIX_SIZE = 16 * 4
_HEADER_SIZE = 8

class E3DInput:
    def __init__(self, file):
        self._chunk_readers = {
            "SUB0": self._read_SUB0,
            "VNT0": self._read_VNT0,
            "TEX0": self._read_zero_separated_chunk,
            "NAM0": self._read_zero_separated_chunk,
            "TRA0": self._read_TRA0,
        }

        self._scanner = BinaryScanner(file)

    def __iter__(self):
        self._scanner.read_bytes(_HEADER_SIZE)

        while not self._scanner.is_empty:
            chunk_id, chunk_size = self._read_header()

            chunk_read = self._chunk_readers.get(chunk_id)

            yield from chunk_read(chunk_size)

    def _read_header(self):
        chunk_id = self._scanner.read_str(4)
        chunk_size = self._scanner.read_int()

        return chunk_id, chunk_size


    def _read_SUB0(self, chunk_size):
        NUM_SUBMODELS = chunk_size // 256

        for _ in range(NUM_SUBMODELS):
            chunk = {}
            #TODO: Dedicated structure
            chunk["next_id"] = self._scanner.read_int()
            chunk["first_child_id"] = self._scanner.read_int()
            chunk["submodel_type_id"] = self._scanner.read_int()
            chunk["name_id"] = self._scanner.read_int()
            chunk["anim_id"] = self._scanner.read_int()
            chunk["flags"] = self._scanner.read_int()
            chunk["transform_id"] = self._scanner.read_int()
            chunk["num_verts"] = self._scanner.read_int()
            chunk["first_vertex_id"] = self._scanner.read_int()
            chunk["material_id"] = self._scanner.read_int()
            chunk["light_level_visibility_treshold"] = self._scanner.read_float()
            chunk["light_emission_treshold"] = self._scanner.read_float()
            chunk["ambient_color"] = [self._scanner.read_float() for _ in range(4)]
            chunk["diffuse_color"] = [self._scanner.read_float() for _ in range(4)]
            chunk["specular_color"] = [self._scanner.read_float() for _ in range(4)]
            chunk["emission_color"] = [self._scanner.read_float() for _ in range(4)]
            chunk["wire_size"] = self._scanner.read_float()
            chunk["max_distance"] = self._scanner.read_float()
            chunk["min_distance"] = self._scanner.read_float()
            chunk["near_atten_start"] = self._scanner.read_float()
            chunk["near_atten_end"] = self._scanner.read_float()
            chunk["use_near_atten"] = self._scanner.read_float()
            chunk["far_atten_decay_type"] = self._scanner.read_float()
            chunk["far_decay_radius"] = self._scanner.read_float()
            chunk["cos_falloff_angle"] = self._scanner.read_float()
            chunk["cos_hotspot_angle"] = self._scanner.read_float()
            chunk["cos_view_angle"] = self._scanner.read_float()

            # skip pad bytes
            self._scanner.read_bytes(100)
            
            yield chunk

    def _read_VNT0(self, chunk_size):
        num_verts = chunk_size // _VERTEX_SIZE
        yield [
            [self._scanner.read_float() for _ in range(8)]
            for _1 in range(num_verts)
        ]

    def _read_TRA0(self, chunk_size):
        num_matrices = chunk_size // _TRA0_MATRIX_SIZE
        yield [
            [self._scanner.read_float() for _ in range(16)]
            for _1 in range(num_matrices)
        ]

    def _read_zero_separated_chunk(self, chunk_size):
        data = self._scanner.read_str(chunk_size - 8)
        values = data.strip("\x00").split("\x00")
        yield values

