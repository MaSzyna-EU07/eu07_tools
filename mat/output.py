from .common import VARIANT_KEYS, FLOAT_KEYS, DEFAULT_VALUES, STRING_KEYS, INT_KEYS
from eu07_tools.utils import TextWriter, TexturePath


def dump(mat, file):
    MATOutput(file).dump_material(mat)


class MATOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)
        self._indent_level = 0

    def dump_material(self, mat):
        self._dump_material(mat, None)

    def _dump_material(self, mat, parent_mat):
        for key, value in mat.items():
            self._write_property(key, value, parent_mat)

    def _write_property(self, key, value, parent_mat=None):
        # TODO:
        # Jeśli w rodzicu zdefiniowana jest jakaś właściwość, a ta sama jest tutaj i mają one te same wartości
        #      nie trzeba zapisać
        # Jeśli mają one różne wartości
        #      to trzeba zapisać
        # Jeśli jakaś wartość jest równa wartości domyślnej a rodzic jej nie definiuje
        #      nie trzeba zapisać
        # Jeśli jakaś wartość jest równa wartości domyślnej i rodzicu zdefiniowana jest, a ta sama jest tutaj i mają one różne wartości
        #       to trzeba zapisać
        #
        # parent_value = parent_mat.get(key)
        # if parent_value is not None:
        #     if param_list == parent_value:
        #         return
        # else:
        #     default_value = DEFAULT_VALUES.get(key)
        #     if (default_value is not None) and default_value == param_list:
        #         return

        self._write_key(key)

        if key in FLOAT_KEYS:
            self._writer.write_float(value)

        elif key in INT_KEYS:
            self._writer.write_int(value)

        elif key in STRING_KEYS:
            self._writer.write_string(value)

        elif key.startswith("texture"):

            if value.is_randomset:
                self._writer.write_string("[")

            self._writer.write_string(
                ", ".join(tpo.path_with_traits for tpo in value.paths)
            )

            if value.is_randomset:
                self._writer.write_string("]")

        elif key.startswith("param"):
            if value:
                self._writer.write_floats(value)

        elif key.startswith("size"):
            self._writer.write_floats(value)

        elif key in VARIANT_KEYS:
            self._write_variant(key, value, parent_mat)

        self._writer.write_string("\n")

    def _write_variant(self, key, variant, parent_mat):
        self._writer.write_string("{\n")

        self._indent_level += 1
        self._dump_material(variant, parent_mat)
        self._indent_level -= 1

        self._writer.write_string("}")

    def _write_key(self, key):
        indent = "\t" * self._indent_level
        self._writer.write_string(f"{indent}{key}:")