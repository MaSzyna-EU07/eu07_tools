from .structures import create_mat_mapping
from eu07_tools.utils import TokenStream


def load(file):
    token_stream = TokenStream.from_file(file)
    return _load_mapping(token_stream)

_NESTED_MAPPING_KEYS = {
    "spring", "summer", "autumn", "winter", 
    "rain", "snow", "cloudy", "clear"
}

_NUMERIC_KEYS = {
    "selfillum", "opacity"
}

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

            if token == "[":
                value = list(token_stream.get_tokens_before("]"))
            else:
                value = token

        elif key in "}{":
            continue
        elif key in _NESTED_MAPPING_KEYS:
            value = _load_mapping(token_stream)
        elif key in _NUMERIC_KEYS:
            value = float(token_stream.get_token())
        elif key == "size":
            value = [float(x) for x in token_stream.get_tokens(2)]
        else:
            value = token_stream.get_token()

        map_[key] = value

    return map_
