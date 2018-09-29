""" Texture files searching facility for MaSzyna Train Simulator """
# TODO: Mat files detection
import os
from typing import Sequence


class TextureSearcher:
    """
    Texture searching management class

    Members:
    _root: str -- MaSzyna installation path
    _file_dir: str -- currently processed file path
    _default_textures_dir: str -- 'textures' directory in root path

    _default_ext: str -- default texture extension
    """
    def __init__(self, root: str, file_dir: str, default_ext: str='tga'):
        self._root = root
        self._file_dir = file_dir
        self._default_textures_dir = os.path.join(self._root, 'textures')
        self._update_lookup_paths()

        self._default_ext = default_ext
        self._extensions = ["tga", "dds", "png", "bmp"]
        self._update_default_extension()

    def find_possible_paths(self, relpath: str) -> Sequence[str]:
        """
        Return list of all existing texture paths.

        Arguments:
        relpath -- relative path to texture (with extension or not)
        """
        relpath = os.path.splitext(relpath)[0]
        relpath = os.path.normpath(relpath.replace('\\', '/')).lstrip('/').lower()

        for lookup_path in self._lookup_paths:
            file_path = os.path.join(lookup_path, relpath)

            for extension in self._extensions:
                full_path = ".".join((file_path, extension))

                if os.path.exists(full_path):
                    yield full_path

    @property
    def default_ext(self) -> str:
        return self._default_ext

    @default_ext.setter
    def default_ext(self, default_ext: str):
        self._default_ext = default_ext
        self._update_extensions()

    @property
    def root(self) -> str:
        return self._root

    @root.setter
    def root(self, root: str):
        self._root = root
        self._update_lookup_paths()

    @property
    def file_dir(self) -> str:
        return self._file_dir

    @file_dir.setter
    def file_dir(self, file_dir: str):
        self._file_dir = file_dir
        self._update_lookup_paths()

    @property
    def default_textures_dir(self) -> str:
        return self._default_textures_dir

    @default_textures_dir.setter
    def default_textures_dir(self, default_textures_dir: str):
        self._default_textures_dir = default_textures_dir
        self._update_lookup_paths()

    def _update_lookup_paths(self):
        """ Update lookup paths list. Called when any lookup path changes """
        self._lookup_paths = [
            self._file_dir, self._root, self._default_textures_dir
        ]

    def _update_default_extension(self):
        """ Update extensions list. Called when default extension changes """
        default_ext_idx = self._extensions.index(self._default_ext)
        self._extensions.pop(default_ext_idx)
        self._extensions.insert(0, self._default_ext)
