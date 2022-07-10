from pathlib import Path

class AssetSearcher:
    def __init__(self, root, basedir=""):
        self._root = Path(root)
        self._basedir = Path(basedir)
        
        self.models = PathFinder(
            [],
            [".e3d", ".t3d"]
        )

        self.textures = PathFinder(
            [],
            [".mat", ".tga", ".dds", ".png", ".bmp", ".tex"]
        )

        self.scenes = PathFinder(
            [],
            []
        )

        self.sounds = PathFinder(
            [],
            [".ogg", ".wav"]
        )

        self.update_lookups()


    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = Path(value)
        self.update_lookups()

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, value):
        self._basedir = Path(value)
        self.update_lookups()

    def update_lookups(self):
        self.models.lookups = [
            Path(self._root),
            Path(self._basedir),
            Path(self._root, "models")
        ]

        self.textures.lookups = [
            Path(self._root),
            Path(self._basedir),
            Path(self._root, "textures"),
            Path(str(self._basedir).replace("models", "textures"))
        ]

        self.scenes.lookups = [
            Path(self._root, "scenery"),
            Path(self._basedir)
        ]

        self.sounds.lookups = [
            Path(self._root, "sounds")
        ]
        


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

    def add_extension(self, extension, priority=0):
        """ 
        Add new extension to extensions list 

        :param extension: Extension to add, with leading dot
        :type extension: `str`
        """
        self.extensions.append(extension)
        self.set_extension_priority(extension, priority)

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
            if lookup == "":
                continue

            full_path = self._lower_filename(Path(lookup, rel_path))

            if self.extensions:
                for extension in self.extensions:
                    full_path = full_path.with_suffix(extension)
                    if full_path.exists():
                        yield str(full_path.with_suffix(extension))
            else:
                if full_path.exists():
                    yield str(full_path)

        return

    def _lower_filename(self, path):
        return Path(path.parent, path.name.lower())
