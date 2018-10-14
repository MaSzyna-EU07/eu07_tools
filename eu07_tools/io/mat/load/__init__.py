from eu07_tools.io.utils import TokenStream

# TODO: Write it more pretty

class MATLoader:
    def __init__(self):
        self._token_stream: TokenStream = None
    
    def load_from_file(self, file):
        self._token_stream = TokenStream.from_file(file)
        material = self._load_block(endmark="")
        return material

    @property
    def progress(self) -> float:
        return self._token_stream.progress
            
    def _load_block(self, endmark: str):
        block = {}
        while True:
            key = self._token_stream.get_token()
            key = key.rstrip(":")

            if key == endmark:
                return block
            elif key == "size":
                value = list(self._token_stream.get_tokens(2))
            else:
                value = self._token_stream.get_token()

                if value.startswith("{"):
                    value = self._load_block(endmark="}")
                elif value.startswith("["):
                    value = list(
                        self._token_stream.get_tokens_before("]")
                    )

            value = self._cast_type(key, value)
                    
            block[key] = value


    def _cast_type(self, key, value):
        if key in "opacity selfillum":
            return float(value)
        if key in ("size"):
            return [float(v) for v in value]
        else:
            return value


