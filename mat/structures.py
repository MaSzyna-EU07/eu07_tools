from eu07_tools.utils import VectorXY
import collections.abc

from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS, DEFAULT_VALUES
from ..utils.structures import TexturePath


def create_material():
    return Material()

class Material:
    def __init__(self):
        self.shader = ""
        self.shader_params = {}
        self.opacity = DEFAULT_VALUES["opacity"]
        self.selfillum = DEFAULT_VALUES["selfillum"]
        self.shadow_rank = DEFAULT_VALUES["shadow_rank"]

        self._texture_paths = {}
        self._variants = {}
        self._size = DEFAULT_VALUES["size"]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = VectorXY(size)

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

