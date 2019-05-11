from pathlib import Path
import functools
import os

class AssetSearcher:
    def __init__(self, root, basedir):
        self._root = Path(root)
        self._basedir = Path(basedir)

        self.models_finder = PathFinder(
            [Path(self._root), Path(self._basedir), Path(self._root, "models")],
            [".e3d", ".t3d"]
        )

        self.textures_finder = PathFinder(
            [Path(self._root), Path(self._basedir), Path(self._root, "textures")],
            [".mat", ".tga", ".dds", ".png", ".bmp", ".tex"]
        )

        self.includes_finder = PathFinder(
            [Path(self._root), Path(self._basedir), Path(self._root, "?")],
            []
        )


class PathFinder:
    """
    Class for finding assets absolute paths.

    :param lookups: sequence of lookup paths. The lookup path is a absolute path to directory, used to concatenate with relative path passed to *find_paths()* method.
    :type lookups: `Sequence[str]`
    :param extensions: sequence of extensions. Each extension should have a leading dot.
    :type extensions: `Sequence[str]` 
    """
    def __init__(self, lookups, extensions):
        self._original_extensions = extensions
        self.extensions = extensions
        self.lookups = lookups

    def reset(self):
        """ Restore default finder state """
        self.extensions = self._original_extensions

    def add_extension(self, extension):
        """ 
        Add new extension to extensions list 

        :param extension: Extension to add, with leading dot
        :type extension: `str`
        """
        self.extensions.append(extension)

    def remove_extension(self, extension):
        """ 
        Remove extension from extensions list 

        :param extension: Extension to remove, with leading dot
        :type extension: `str`
        """
        self.extensions.remove(extension)

    def set_extension_priority(self, extension, priority):
        """ 
        Set extension priority in extensions list.
        The highest priority is 0.

        :param extension: extension, with leading dot
        :type extension: `str`
        :param priority: priority 
        """
        self.extensions.pop(self.get_extension_priority(extension))
        self.extensions.insert(priority, extension)

    def get_extension_priority(self, extension):
        """
        Get extension priority

        :param extension: extension, with leading dot
        :type extension: `str`

        :returns: priority of given extension
        :rtype: `int`
        """
        return self.extensions.index(extension)

    def find_paths(self, rel_path):
        """
        Find all possible asset paths.

        :param rel_path: relative path to asset
        :type rel_path: `str`

        :returns: iterator of all possible absolute asset paths.
        :rtype: `Iterator[str]`
        """
        
        for lookup in self.lookups:
            full_path = Path(lookup, rel_path)

            if self.extensions:
                for extension in self.extensions:
                    yield str(full_path.with_suffix(extension))
            else:
                yield str(full_path)