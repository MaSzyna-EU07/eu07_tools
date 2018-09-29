from collections import namedtuple
from functools import partial
import struct
from typing import Tuple


MATRIX_SIZE = 64
VERTEX_SIZE = 32
SUB0_SIZE = 256
CHUNK_HEADER_SIZE = 8
INT_SIZE = 4
FLOAT_SIZE = 4



type_id_to_name = {
    4: 'Mesh',
    256: 'Mesh',
    257: 'FreeSpotLight',
    258: 'Stars'
}

anim_id_to_name = {
    -1: 'true',
    0: 'false',
    4: 'seconds_jump',
    5: 'minutes_jump',
    6: 'hours_jump',
    7: 'hours24_jump',
    8: 'seconds',
    9: 'minutes',
    10: 'hours',
    11: 'hours24',
    12: 'billboard',
    13: 'wind',
    14: 'sky',
    256: 'ik',
    257: 'ik1',
    258: 'ik2'
}



class E3DChunksParser:
    def __init__(self):
        self.submodels = []
        self.vertices = []
        self.textures = []
        self.names = []
        self.transforms = []

        self._chunk_loaders = {
            'SUB0': self._load_submodels,
            'VNT0': self._load_vertices,
            'TEX0': self._load_textures,
            'NAM0': self._load_names,
            'TRA0': self._load_transforms,
        }


    def load(self, file_):
        self._file = file_

        __, main_chunk_size = self._unpack_chunk_header()
        file_size = main_chunk_size + CHUNK_HEADER_SIZE

        while file_.tell() < file_size:
            chunk_id, chunk_size = self._unpack_chunk_header()

            load_chunk = self._chunk_loaders[chunk_id]
            yield load_chunk(chunk_size)

    def _unpack_chunk_header(self) -> Tuple[str, int]:
        buffer = struct.unpack('4s I', self._file.read(CHUNK_HEADER_SIZE))
        chunk_id = buffer[0].decode('utf-8')
        size = buffer[1] - CHUNK_HEADER_SIZE # Chunk header is already readed - we are interest only with data size
        return chunk_id, size

    def _unpack_int(self) -> int:
        buffer = struct.unpack('i', self._file.read(INT_SIZE))
        return buffer[0]

    def _unpack_float(self) -> float:
        buffer = struct.unpack('f', self._file.read(FLOAT_SIZE))
        return buffer[0]

    def _unpack_rgba(self) -> float:
        buffer = struct.unpack('4f', self._file.read(4 * FLOAT_SIZE))
        return buffer

    def _read_submodel(self, chunk_size: int):
        num_submodels = chunk_size // SUB0_SIZE

        submodel_record = {}

        for _ in range(num_submodels):
            submodel_record['id_next'] = self._unpack_int()
            submodel_record['id_first_child'] = self._unpack_int()
            submodel_record['id_type'] = self._unpack_int()
            submodel_record['id_name'] = self._unpack_int()
            submodel_record['id_anim'] = self._unpack_int()
            submodel_record['flags'] = self._unpack_int()
            submodel_record['id_transform'] = self._unpack_int()
            submodel_record['num_verts'] = self._unpack_int()
            submodel_record['id_first_vertex'] = self._unpack_int()
            submodel_record['id_texture'] = self._unpack_int()
            submodel_record['threshold_light_on'] = self._unpack_float()
            submodel_record['selfillum'] = self._unpack_float()
            submodel_record['ambient'] = self._unpack_rgba()
            submodel_record['diffuse'] = self._unpack_rgba()
            submodel_record['specular'] = self._unpack_rgba()
            submodel_record['emission_color'] = self._unpack_rgba()
            submodel_record['wire_size'] = self._unpack_float()
            submodel_record['max_distance'] = self._unpack_float()
            submodel_record['min_distance'] = self._unpack_float()
            submodel_record['near_atten_start'] = self._unpack_float()
            submodel_record['near_atten_end'] = self._unpack_float()
            submodel_record['use_near_atten'] = self._unpack_float()
            submodel_record['far_atten_decay_type'] = self._unpack_int()
            submodel_record['far_decay_radius'] = self._unpack_float()
            submodel_record['falloff_angle'] = self._unpack_float()  # Cosinus here
            submodel_record['hotspot_angle'] = self._unpack_float()  # Cosinus here
            submodel_record['view_angle'] = self._unpack_float()  # Dafuq is that?

            # Skip pad bytes
            self._file.seek(self._file.tell() + 100)

    def _read_vertices(self, chunk_size: int):
        num_verts = chunk_size // VERTEX_SIZE

        for _ in range(num_verts):
            vertex = struct.unpack('8f', self._file.read(VERTEX_SIZE))
            self.vertices.append(vertex)

    def _read_textures(self, chunk_size: int):
        self.textures = self._read_zero_separated_chunk(chunk_size)

    def _read_names(self, chunk_size: int):
        self.names = self._read_zero_separated_chunk(chunk_size)

    def _read_transforms(self, chunk_size: int):
        num_matrices = chunk_size // MATRIX_SIZE

        for _ in range(num_matrices):
            unpacked = list(struct.unpack('16f', self._file.read(MATRIX_SIZE)))
            matrix = [
                unpacked[:4],
                unpacked[4:8],
                unpacked[8:12],
                unpacked[12:]
            ]
            self.transforms.append(matrix)

    def _read_zero_separated_chunk(self, chunk_size: int) -> Sequence[str]:
        chunk_format = '{}s'.format(chunk_size)
        buffer = self._file.read(chunk_size)
        unpacked = struct.unpack(chunk_format, buffer)[0]
        values = unpacked.decode('utf-8').strip('\x00').split('\x00')
        return values
