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
        token = scanner.get_token()
        key = token.rstrip(":")
        value = None
        
        if not token:
            break
        elif key == "{":
            continue
        elif key == "}":
            break 


        elif "texture" in key:
            token = scanner.get_token()

            if token == "[":
                value = list(scanner.get_tokens_before("]"))
            else:
                value = token

        elif key in NESTED_MAPPING_KEYS:
            value = _load_mapping(scanner)
        elif key in NUMERIC_KEYS:
            value = float(scanner.get_token())
        elif key == "size":
            value = [float(x) for x in scanner.get_tokens(2)]
        else:
            value = scanner.get_token()

        map_[key] = value

    return map_
