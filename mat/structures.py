from eu07_tools.utils import VectorXY
import collections.abc

from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS
from ..utils.structures import TexturePath


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


class Material:
    def __init__(self):
        self.shader = ""
        self.shader_params = {}
        self.opacity = 1
        self.selfillum = -1
        self.shadow_rank = 3

        self._texture_paths = {}
        self._variants = {}
        self._size = VectorXY(-1, -1)

    def set_variant(self, key, mat_variant):
        self._variants[key] = mat_variant

    def get_variant(self, key):
        return self._variants.get(key)

    def create_variant(self, key):
        mat_variant = Material()
        self._variants[key] = mat_variant

    def remove_variant(self, key):
        del self._variants[key]

    def iter_variants(self):
        for key, variant in self._variants.items():
            yield key, variant

    def set_textureset(self, key, paths):
        self._texture_paths[key] = [TexturePath(p) for p in paths]

    def get_textureset(self, key):
        return self._texture_paths.get(key)

    def set_texture_path(self, key, path):
        self._texture_paths[key] = [TexturePath(path)]

    def get_texture_path(self, key):
        paths = self._texture_paths.get(key)
        if paths:
            return paths[0]

    def remove_texture(self, key):
        del self._variants[key]

    def iter_texture_lists(self):
        for key, tex in self._texture_paths.items():
            yield key, tex

