from maszyna_utils.structs.scn import (
    SCNAtmo
)

class SCNLoader:
    def __init__(self):
        self._entry_loaders = {
            'atmo': self._load_atmo,
            'camera': self._load_camera,
        }

    def load_scenery(self, filepath: str):
        self._token_stream = Tokenizer().tokenize(filepath)

        while True:
            token = self._token_stream.get_token()

            if token is None:
                break

            load_entry = self._entry_loaders[token.lower()]

            entry = load_entry()

            yield entry

    def _load_atmo(self):
        atmo_color = self._token_stream.get_tokens(3)
        atmo_color = [float(value) for value in atmo_color]

        fog_start = float(self._token_stream.get_token())
        fog_end = float(self._token_stream.get_token())

        fog_color = None
        if fog_end > 0:
            fog_color = self._token_stream.get_tokens(3)
            fog_color = [float(value) for value in fog_color]

        overcast = float(self._token_stream.get_token())

        return SCNAtmo(
            atmo_color, fog_start, fog_end, fog_color, overcast
        )
