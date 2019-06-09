from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS

def dump(mapping, file):
    _dump_mapping(mapping, file)




class _MATDumper:
    def __init__(self, mapping, file):
        self._file = file
        self._indent = -1
        self._mapping = mapping
    
    def dump_mapping():
    _write_if_exists("texture_diffuse")
    _write_if_exists("texture0")
    _write_if_exists("texture_normal")
    _write_if_exists("texture1")

    _write_if_exists("shader")
    _write_shader_params()

    _write_if_exists("opacity")
    _write_if_exists("selfillum")
    _write_if_exists("size")

    _write_if_exists("spring")
    _write_if_exists("summer")
    _write_if_exists("autumn")
    _write_if_exists("winter")

    _write_if_exists("clear")
    _write_if_exists("cloudy")
    _write_if_exists("rain")
    _write_if_exists("snow")

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

    
