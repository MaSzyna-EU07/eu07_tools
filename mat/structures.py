from eu07_tools.utils import VectorXY
import collections.abc

from .common import VARIANT_KEYS, FLOAT_KEYS, DEFAULT_VALUES
from ..utils.structures import TexturePath


def create_material():
    return MATMaterial()

class MATMaterial:
    def __init__(self):
        self._items = {}

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        if key == "size":
            value = VectorXY(value)

        self._items[key] = value

    def get_default_shader_name(self):
        num_textures = len([k for k in self.keys() if k.startswith("texture")])
        return f"default_{num_textures}"

    def get(self, key, default=None):
        return self._items.get(key, default)

    def items(self):
        for key, value in self._items.items():
            yield key, value

    def keys(self):
        for k in self._items.keys():
            yield k

    def values(self):
        for v in self._items.values():
            yield v


class MATTextureValue:
    def __init__(self, *paths):
        self.paths = [p for p in paths]

    @classmethod
    def from_list(cls, pathlist):
        return cls(*pathlist)

    @classmethod
    def from_path(cls, string):
        return cls(string)

    @property
    def is_randomset(self):
        return len(self.paths) > 1

    @property
    def is_path(self):
        return len(self.paths) == 1

    @property
    def is_empty(self):
        return len(self.paths) == 0
