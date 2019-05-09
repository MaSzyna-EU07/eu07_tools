from eu07_tools.utils import VectorXY
from collections.abc import MutableMapping

class MATMaterial(MutableMapping):
    def __init__(self, path):
        self.filepath = ""
        self._mapping = MATMapping()

    def __getitem__(self, key):
        return self._mapping[key]

    
class MATMapping(MutableMapping):
    # TODO: Dict-like interface
    # TODO: Random textures, how to handle this shit?
    def __init__(self):
        self._mapping = {
            "spring": MATMapping(),
            "summer": MATMapping(),
            "autumn": MATMapping(),
            "winter": MATMapping(),

            "clear": MATMapping(),
            "cloudy": MATMapping(),
            "rain": MATMapping(),
            "snow": MATMapping(),
        }

    def __getitem__(self, key):
        return self._mapping[key]


    def __setitem__(self, key, value):
        if key == "size":
            self._mapping["size"] = VectorXY(value)

    def __iter__(self):
        for key in self._mapping:
            yield key

class TexturePath:
    def __init__(self, path):
        self._path = path

        if path.startswith("make:"):
            self.type = "GENERATED"
        elif path.startswith("[") and path.endswith("]"):
            self.type = "RANDOM_SET"
        elif path in "replacableskin -1 -2 -3 -4":
            self.type = "SKIN"
        else:
            self.type = "IMAGE"

    def __str__(self):
        return self._path

    
        

        