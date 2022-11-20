from eu07_tools.utils import VectorXY
import collections.abc

from .common import NESTED_MAPPING_KEYS, FLOAT_KEYS, DEFAULT_VALUES
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

    def get(self, key, default=None):
        return self._items.get(key, default)

    def create_texture_path_object(self, path):
        return TexturePath(path)

    def create_variant(self):
        return MATMaterial()

    def items(self):
        for key, value in self._items.items():
            yield key, value

    def keys(self):
        for k in self._items.keys():
            yield k

    def values(self):
        for v in self._items.values():
            yield v
