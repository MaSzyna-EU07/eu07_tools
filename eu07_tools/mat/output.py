from collections.abc import MutableMapping

class MATOutput:
    @classmethod
    def to_file(self, file):
        return MATOutput(file)

    def __init__(self, file):
        self._file = file

    def dump_material(self, material):
        indent_level = 0
        self._dump_mapping(material, indent_level)

    def _dump_mapping(self, mapping, indent_level):
        # TODO: should be iteritems
        for key in mapping:
            value = mapping[key]
            if isinstance(value, MutableMapping):
                self._file.write("\t" * indent_level + "{key}: {\n")
                self._dump_mapping(value, indent_level + 1)
                self._file.write("\t" * indent_level + "}\n")
            elif isinstance(value, ):
                self._file.write("\t" * indent_level + "{key}: {value}")