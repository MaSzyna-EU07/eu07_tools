from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS, DEFAULT_VALUES, STRING_KEYS
from eu07_tools.utils import TextWriter


def dump(mat, file):
    MATOutput(file).dump_material(mat)


class MATOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)
        self._indent_level = 0

    def dump_material(self, mat):
        self._dump_material(mat, None)

    def _dump_material(self, mat, parent_mat):
        parent_shader = parent_mat.shader if parent_mat else None
        self._write_property("shader", mat.shader, parent_shader)

        for param_key, param_array in mat.shader_params:
            self._write_key(param_key)
            self._writer.write_floats(param_array)
            self._writer.write_string("\n")

        for texture_key, pathlist in mat.iter_texture_lists():
            self._write_property(texture_key, [p.path_with_traits for p in pathlist])

        parent_opacity = parent_mat.opacity if parent_mat else None
        self._write_property("opacity", mat.opacity, parent_opacity)

        parent_selfillum = parent_mat.selfillum if parent_mat else None
        self._write_property("selfillum", mat.selfillum, parent_selfillum)

        parent_size = parent_mat.size if parent_mat else None
        self._write_property("size", mat.size, parent_size)

        parent_shadowrank = parent_mat.shadow_rank if parent_mat else None
        self._write_property("shadow_rank", mat.shadow_rank, parent_shadowrank)

        self._indent_level += 1

        for variant_name, variant in mat.iter_variants():
            self._write_variant(variant_name, variant, mat)

        self._indent_level -= 1

    def _write_property(self, key, value, parent_value=None):
        if (parent_value is not None) and value == parent_value:
            return

        default_value = DEFAULT_VALUES.get(key)
        if (default_value is not None) and default_value == value:
            return

        self._write_key(key)

        if key in NUMERIC_KEYS:
            self._writer.write_float(value)
        elif key in STRING_KEYS:
            self._writer.write_string(value)
        elif key.startswith("texture"):
            pathcount = len(value)

            if pathcount == 1:
                self._writer.write_string(value[0])
            elif pathcount > 1:
                self._writer.write_string("[")
                self._writer.write_floats(value)
                self._writer.write_string("]")

        else:
            self._writer.write_floats(value)

        self._writer.write_string("\n")

    def _write_variant(self, key, variant, parent_mat):
        self._indent_level -= 1
        self._write_key(key)
        self._indent_level += 1
        self._writer.write_string("{\n")

        self._dump_material(variant, parent_mat)

        self._writer.write_string("}\n")

    def _write_key(self, key):
        indent = "\t" * self._indent_level
        self._writer.write_string(f"{indent}{key}:")