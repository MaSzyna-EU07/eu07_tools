from .structures import create_mat_mapping
from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS
from eu07_tools.utils import TokenStream


def load(file):
    token_stream = TokenStream.from_file(file)
    return _load_mapping(token_stream)

# TODO: Texturesets
def _load_mapping(token_stream):
    map_ = create_mat_mapping()

    while True:
        token = token_stream.get_token()
        key = token.rstrip(":")
        value = None

        if not token:
            break
        elif "texture" in key:
            token = token_stream.get_token()

            # Unify naming
            key = key.replace("0", "_diffuse")
            key = key.replace("1", "_normal")

            if token == "[":
                value = list(token_stream.get_tokens_before("]"))
            else:
                value = token

        elif key in "}{":
            continue
        elif key in NESTED_MAPPING_KEYS:
            value = _load_mapping(token_stream)
        elif key in NUMERIC_KEYS:
            value = float(token_stream.get_token())
        elif key == "size":
            value = [float(x) for x in token_stream.get_tokens(2)]
        else:
            value = token_stream.get_token()

        map_[key] = value

    return map_
