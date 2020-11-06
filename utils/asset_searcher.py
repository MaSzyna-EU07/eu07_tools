from pathlib import Path


class AssetSearcher:
    def __init__(self, root, basedir):
        self._root = Path(root)
        self._basedir = Path(basedir)

        self.models = PathFinder(
            [
                Path(self._root), 
                Path(self._basedir), 
                Path(self._root, "models")
            ],
            [".e3d", ".t3d"]
        )

        self.textures = PathFinder(
            [
                Path(self._root), 
                Path(self._basedir), 
                Path(self._root, "textures"),
                Path(str(self._basedir).replace("models", "textures"))
            ],
            [".mat", ".tga", ".dds", ".png", ".bmp", ".tex"]
        )

        self.includes = PathFinder(
            [
                Path(self._root), 
                Path(self._basedir)
            ],
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

    def find(self, rel_path):
        try:
            return next(self.find_all(rel_path))
        except StopIteration:
            return ""
        
    def find_all(self, rel_path):
        """
        Find all existing assets paths.

        :param rel_path: relative path to asset
        :type rel_path: `str`

        :returns: iterator of paths
        :rtype: `Iterator[str]`
        """
        
        rel_path = rel_path.lstrip("\\").lstrip("/")
        rel_path = rel_path.replace("\\", "/")
        for lookup in self.lookups:
            full_path = Path(lookup, rel_path)

            if self.extensions:
                for extension in self.extensions:
                    full_path = full_path.with_suffix(extension)
                    full_path_lowered = Path(str(full_path).lower())
                    if full_path.exists() or full_path_lowered.exists():
                        yield str(full_path.with_suffix(extension))
            else:
                full_path_lowered = Path(str(full_path).lower())
                if full_path.exists() or full_path_lowered.exists():
                    yield str(full_path)

        return