from eu07_tools.utils import VectorXY
import collections.abc

from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS


def create_mapping():
    return Mapping()

class Mapping(collections.abc.MutableMapping):
    def __init__(self):
        self._items = {}

    @classmethod
    def from_dict(cls, d):
        map_ = create_mapping()
        for k, v in d.items():
            map_[k] = v

        return map_

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        if key == "size":
            self._items["size"] = VectorXY(value)
        elif "texture" in key:
            tex_value = self._items[key] = MATTextureValue()
            if isinstance(value, str):
                tex_value.path = value
                tex_value.use_set = False
            else:
                tex_value.set = list(value)
                tex_value.use_set = True
        else:
            self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

class MATTextureValue:
    def __init__(self):
        self.path = ""
        self.set = []
        self.use_set = False

    def __str__(self):
        if self.use_set:
            return "[ " + " ".join(self.set) + " ]"
        else:
            return self.path



