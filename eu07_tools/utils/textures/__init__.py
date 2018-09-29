import os

from .searcher import TextureSearcher

__all__ = ['make_relative_path', 'TextureSearcher']

def make_relative_path(current_file_path: str, abspath: str, root: str) -> str:
    """ Return relative texture path normalized for MaSzyna assets """
    current_file_dir = os.path.dirname(os.path.normpath(current_file_path))
    abspath = os.path.normpath(abspath)
    root = os.path.normpath(root)

    if '/dynamic/' in abspath:
        current_dynamic_directory = os.path.dirname(current_file_dir)
        relpath = os.path.relpath(abspath, current_dynamic_directory)
    elif '/textures/' in abspath:
        textures_directory = os.path.join(root, 'textures')
        relpath = os.path.relpath(abspath, textures_directory)
    else:
        relpath = os.path.relpath(abspath, root)

    relpath = relpath.replace('\\', '/')
    relpath = os.path.splitext(relpath)[0]

    return '/' + relpath
