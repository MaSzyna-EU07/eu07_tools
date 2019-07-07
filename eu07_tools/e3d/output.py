from eu07_tools.utils import BinaryWriter

from .common import SUBMODEL_SIZE

class E3DOutput:
    def __init__(self, file, model):
        self._writer = BinaryWriter(file)
        self._model = model

    def dump(self):
        self._writer.write_string("E3D0")
        self._writer.write_int(0) # TODO: Calculate e3d0 chunk size
        self._dump_SUB0()
        self._dump_VNT0()

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
            self._writer.write_pad_bytes(100)

    def _dump_VNT0(self):
        for vertex in self._model.vertices:
            self._writer.write_float_list(vertex)

    def _dump_TEX0(self)