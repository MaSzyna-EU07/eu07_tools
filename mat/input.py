from .structures import create_mapping
from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS
from eu07_tools.utils import TextScanner


def load(file):
    scanner = TextScanner.from_file(file)
    return _load_mapping(scanner)

# TODO: Texturesets
def _load_mapping(scanner):
    map_ = create_mapping()

    while True:
        token = scanner.read_string()
        key = token.rstrip(":")
        value = None
        
        if not token:
            break
        elif key == "{":
            continue
        elif key == "}":
            break 


        elif "texture" in key:
            token = scanner.read_string()

            if token == "[":
                value = list(scanner.read_strings_before("]"))
            else:
                value = token

        elif key in NESTED_MAPPING_KEYS:
            value = _load_mapping(scanner)
        elif key in NUMERIC_KEYS:
            value = scanner.read_float()
        elif key == "size":
            value = [float(x) for x in scanner.read_floats(2)]
        elif key.startswith("param"):
            value = []
            while 1:
                token = scanner.read_string()
                try:
                    pv = float(token)
                except ValueError:
                    scanner.put_back(token)
                    break
                else:
                    value.append(pv)


        else:
            value = scanner.read_string()

        map_[key] = value

    return map_
