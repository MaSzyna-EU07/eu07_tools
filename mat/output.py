from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS, DEFAULT_VALUES, STRING_KEYS
from eu07_tools.utils import TextWriter


def dump(mapping, file):
    MATOutput(file).dump_mapping(mapping)

class MATOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)
        self._indent_level = 0
    
    def dump_mapping(self, mapping):
        self._dump_mapping(mapping)

    def _dump_mapping(self, mapping):
        self._write_value_if_exists(mapping, "shader")
        self._write_shader_params(mapping)

        texture_keys = [key for key in mapping.keys() if key.startswith("texture")]

        for key in texture_keys:
            self._write_value_if_exists(mapping, key)

        self._write_value_if_exists(mapping, "shadow_rank")
        self._write_value_if_exists(mapping, "opacity")
        self._write_value_if_exists(mapping, "selfillum")
        self._write_value_if_exists(mapping, "size")

        self._indent_level += 1

        for key in NESTED_MAPPING_KEYS:
            self._write_submapping(key, mapping)

        self._indent_level -= 1

    def _write_value_if_exists(self, mapping, key):
        value = mapping.get(key)

        if value is None:
            return

        default_value = DEFAULT_VALUES.get(key)
        if default_value and default_value == value:
            return

        self._write_key(key)

        if key in NUMERIC_KEYS:
            self._writer.write_float(value)
        elif key in STRING_KEYS:
            self._writer.write_string(value)
        elif key.startswith("texture"):
            self._writer.write_string(str(value))
        else:
            self._writer.write_floats(value)


        self._writer.write_string("\n")

    def _write_submapping(self, key, mapping):
        submapping = mapping.get(key)

        if submapping:
            self._indent_level -= 1
            self._write_key(key)
            self._indent_level += 1
            self._writer.write_string("{\n")

            self._dump_mapping(submapping)

            self._writer.write_string("}\n")

    def _write_shader_params(self, mapping):
        for key in mapping:
            if key.startswith("param"):
                self._write_key(key)
                self._writer.write_floats(mapping[key])
                self._writer.write_string("\n")

    def _write_key(self, key):
        indent = "\t" * self._indent_level
        self._writer.write_string(f"{indent}{key}:")
    
