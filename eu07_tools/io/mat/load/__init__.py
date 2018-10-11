from eu07_tools.io.utils import TokenStream

class MATLoader:
    def __init__(self):
        self._token_stream: TokenStream = None
    
    def load_from_file(self, file):
        self._token_stream = TokenStream.from_file(file)
        material = {}

        while True:
            key, value = self._token_stream.get_tokens(2)

            if key == "":
                return material
            if value.startswith("{"):
                pass
            elif value.startswith("["):
                pass
            else:
                pass    
                
            key = key.rstrip(":")
            material[key] = value
        