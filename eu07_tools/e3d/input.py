import struct

#TODO: Refactor magic numbers
def load(file):
    inp = E3DInput.from_file(file)
    return inp
    
_VERTEX_SIZE = 32
_TRA0_MATRIX_SIZE = 16
_TRA1_MATRIX_SIZE = 32

class E3DInput:
    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __init__(self, file):
        self._chunk_readers = {
            "SUB0": self._read_SUB0,
            "VNT0": self._read_VNT0,
            "TEX0": self._read_TEX0,
            "NAM0": self._read_zero_separated_chunk,
            "TRA0": self._read_TRA0,
            "TRA1": self._read_TRA1
        }

        self._scanner = E3DScanner(file)
        

    def __iter__(self):
        while not self._scanner.is_empty:
            chunk_id = self._scanner.read_str(4)
            chunk_size = self._scanner.read_int()

            print("CID:", chunk_id, chunk_size)
            chunk_read = self._chunk_readers.get(chunk_id)
            chunk_data = chunk_read(chunk_size)
            print(chunk_data)
            yield chunk_id, chunk_data

        print("eof")


    def _read_SUB0(self, chunk_size):
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
        chunk["ambient_color"] = self._scanner.read_floats(4)
        chunk["diffuse_color"] = self._scanner.read_floats(4)
        chunk["specular_color"] = self._scanner.read_floats(4)
        chunk["emission_color"] = self._scanner.read_floats(4)
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
        self._scanner.read(100)
        
        return chunk

    def _read_VNT0(self, chunk_size):
        num_verts = chunk_size // _VERTEX_SIZE
        return [
            self._scanner.read_floats(8) for _ in range(num_verts)
        ] 

    def _read_TRA0(self, chunk_size):
        num_matrices = chunk_size // _TRA0_MATRIX_SIZE
        return [
            self._scanner.read_floats(_TRA0_MATRIX_SIZE) for _ in range(num_matrices)
        ] 

    def _read_TRA1(self, chunk_size):
        num_matrices = chunk_size // _TRA1_MATRIX_SIZE
        return [
            self._scanner.read_floats(_TRA1_MATRIX_SIZE) for _ in num_matrices
        ] 

    def _read_TEX0(self, chunk_size):
        return self._read_zero_separated_chunk(chunk_size - 8)

    def _read_zero_separated_chunk(self, chunk_size):
        data = self._scanner.read_str(chunk_size)
        values = data.strip("\x00").split("\x00")
        return values

class E3DScanner:
    def __init__(self, file):
        self._file = file
        __, self._file_size = self.read(4), (self.read_int() + 4)

    @property
    def is_empty(self):
        print("file size", self._file_size, "pos", self._file.tell())
        return self._file_size <= self._file.tell()

    def read(self, n):
        self._file.read(n)

    def read_int(self):
        return struct.unpack("i", self._file.read(4))[0]

    def read_float(self):
        return struct.unpack("f", self._file.read(4))[0]

    def read_str(self, length):
        return struct.unpack(f"{length}s", self._file.read(length))[0].decode("utf-8")

    def read_floats(self, length):
        return [self.read_float() for _ in range(length)]