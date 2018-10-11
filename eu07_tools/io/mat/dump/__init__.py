from typing import Dict, Any
from io import StringIO

# TODO: Cleanup, now this code is terrible, but it works

class MATDumper:
    def __init__(self, file):
        self._file = file

    def dump_material_dict(self, dict_: Dict[str, Any]):
        self._file.write(self._block_to_string(dict_))

    def _block_to_string(self, block_dict: Dict[str, Any], indent: int=0, in_brackets=False):
        buffer = StringIO()
        if in_brackets:
            buffer.write("{\n")
        for key, value in block_dict.items():
            if isinstance(value, dict):
                value = self._block_to_string(value, indent=indent+1, in_brackets=True)
            elif isinstance(value, (tuple, list)):
                value = " ".join(str(v) for v in value)
            elif isinstance(value, set):
                value = f"[ {' '.join(str(v) for v in value)} ]"

            indentation = '\t' * indent
            buffer.write(f"{indentation}{key}: {value}\n")
        if in_brackets:
            indentation = "\t" * (indent - 1) 
            buffer.write(f"{indentation}" + "}")

        return buffer.getvalue()