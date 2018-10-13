from typing import Dict, Any
import collections
from io import StringIO

# TODO: Cleanup, now this code is terrible, but it works

class MATDumper:
    def __init__(self, file):
        self._file = file

    def dump_material_dict(self, dict_: Dict[str, Any]):
        self._file.write(self._block_to_string(dict_))

    def _block_to_string(self, block_dict: Dict[str, Any], indent: int=0, in_brackets=False):
        buffer = StringIO()

        for key, value in block_dict.items():
            
            value_is_list = isinstance(value, list)
            value_is_block = isinstance(value, dict)

            if value_is_block:
                value = self._block_to_string(value, indent=indent+1, in_brackets=True)
            elif value_is_list:
                value = " ".join(str(v) for v in value)
                value = f"[ {value} ]" if "texture" in key else value
                    
            indentation = '\t' * indent
            buffer.write(f"{indentation}{key}: {value}\n")

        string = buffer.getvalue()

        if in_brackets:
            indentation = "\t" * (indent - 1)
            string = (
                "{\n" +
                string +
                indentation + "}"
            )
    
        return string