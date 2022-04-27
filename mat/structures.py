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
            self._items[key] = Texture(value)
        else:
            self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

class Texture:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.value_type = (
            "TEXTURE_SET" if isinstance(value, list)
            else "TEXTURE_PATH"
        )
        self._value = value

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"type={self.value_type} "
            f"value={self.value}>"
        )

    def __str__(self):
        if self.value_type == "TEXTURE_SET":
            return "[ " + " ".join(self._value) + " ]"
        else:
            return self.value

