from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS

def dump(mapping, file):
    MATOutput.dump_mapping(mapping, file)

class MATOutput:
    def __init__(self, mapping, file):
        self._file = file
        self._indent = -1
        self._mapping = mapping
    
    def dump_mapping():
        self._write_if_exists("texture_diffuse")
        self._write_if_exists("texture0")
        self._write_if_exists("texture_normal")
        self._write_if_exists("texture1")

        self._write_if_exists("shader")
        self._write_shader_params()

        self._write_if_exists("opacity")
        self._write_if_exists("selfillum")
        self._write_if_exists("size")

        self._write_if_exists("spring")
        self._write_if_exists("summer")
        self._write_if_exists("autumn")
        self._write_if_exists("winter")

        self._write_if_exists("clear")
        self._write_if_exists("cloudy")
        self._write_if_exists("rain")
        self._write_if_exists("snow")

    def _write_if_exists(key):
        value = mapping.get(key)

        if not value:
            return

        if key in NESTED_MAPPING_KEYS:
            _dump_mapping(value, file, indent+1)

    def _write_shader_params(mapping, file):
        for key in mapping:
            if key.startswith("param"):
                _write_if_exists(mapping, key)

    
