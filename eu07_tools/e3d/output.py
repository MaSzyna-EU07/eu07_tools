from eu07_tools.utils import BinaryWriter

from .common import SUBMODEL_SIZE, VERTEX_SIZE, MATRIX_SIZE, CHUNK_HEADER_SIZE

class E3DOutput:
    def __init__(self, file, model):
        self._writer = BinaryWriter(file)
        self._file = file
        self._model = model

    def dump(self):
        self._writer.write_string("E3D0")

        self._dump_SUB0()
        self._dump_VNT0()
        self._dump_TEX0()
        self._dump_NAM0()
        self._dump_TRA0()
        
        # Get E3D0 data size and write it
        self._file.seek(0, 2)
        size = self._file.tell() - (CHUNK_HEADER_SIZE - 4)
        self._file.seek(4, 0)

        self._writer.write_int(size)

    def _dump_SUB0(self):
        self._writer.write_string("SUB0")
        chunk_size = len(self._model.submodels) * SUBMODEL_SIZE
        self._writer.write_int(chunk_size)

        for submodel in self._model.submodels:
            self._writer.write_int(submodel.next_id)
            self._writer.write_int(submodel.first_child_id)
            self._writer.write_int(submodel.submodel_type_id)
            self._writer.write_int(submodel.name_id)
            self._writer.write_int(submodel.anim_id)
            self._writer.write_int(submodel.flags)
            self._writer.write_int(submodel.matrix_id)
            self._writer.write_int(submodel.num_verts)
            self._writer.write_int(submodel.first_vertex_id)
            self._writer.write_int(submodel.material_id)
            self._writer.write_float(submodel.visibility_light_treshold)
            self._writer.write_float(submodel.selfillum)
            self._writer.write_float_list(submodel.ambient_color)
            self._writer.write_float_list(submodel.diffuse_color)
            self._writer.write_float_list(submodel.specular_color)
            self._writer.write_float_list(submodel.emission_color)
            self._writer.write_float(submodel.wire_size)
            self._writer.write_float(submodel.max_distance)
            self._writer.write_float(submodel.min_distance)
            self._writer.write_float(submodel.near_atten_start)
            self._writer.write_float(submodel.near_atten_end)
            self._writer.write_float(submodel.use_near_atten)
            self._writer.write_float(submodel.far_atten_decay_type)
            self._writer.write_float(submodel.far_decay_radius)
            self._writer.write_float(submodel.cos_falloff_angle)
            self._writer.write_float(submodel.cos_hotspot_angle)
            self._writer.write_float(submodel.cos_view_angle)
            self._writer.write_bytes(b"\0" * 100)

    def _dump_VNT0(self):
        self._writer.write_string("VNT0")
        chunk_size = len(self._model.vertices) * VERTEX_SIZE
        self._writer.write_int(chunk_size)

        for vertex in self._model.vertices:
            self._writer.write_float_list(vertex)

    def _dump_TEX0(self):
        if self._model.materials:
            self._writer.write_string("TEX0")
            chunk_size = sum((len(m) for m in self._model.materials)) + len(self._model.materials) + 1
            self._writer.write_int(chunk_size)

            self._writer.write_bytes(b"\0")
            for material in self._model.materials:
                self._writer.write_string(material)
                self._writer.write_bytes(b"\0")

    def _dump_NAM0(self):
        if self._model.names:
            self._writer.write_string("NAM0")
            chunk_size = sum((len(m) for m in self._model.materials)) + len(self._model.materials)
            self._writer.write_int(chunk_size)

            for name in self._model.names:
                self._writer.write_string(name)
                self._writer.write_bytes(b"\0")

    def _dump_TRA0(self):
        self._writer.write_string("TEX0")
        chunk_size = len(self._model.matrices) * MATRIX_SIZE
        self._writer.write_int(chunk_size)

        for matrix in self._model.matrices:
            self._writer.write_float_list(matrix)