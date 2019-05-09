from pathlib import Path
import os


class AssetSearcher:
    def __init__(self, extensions, lookups):
        self._original_extensions = extensions
        self.extensions = extensions
        self.lookups = lookups

    def reset(self):
        self.extensions = self._original_extensions

    def set_extension_priority(self, extension, priority):
        self.extensions.pop(self.get_extension_priority(extension))
        self.extensions.insert(priority, extension)

    def get_extension_priority(self, extension):
        return self.extensions.index(extension)

    def find_paths(self, rel_path):
        for lookup in self.lookups:
            full_path = Path(lookup, rel_path)
            for extension in self.extensions:
                yield str(full_path.with_suffix(extension))



class AssetSearcher:
    def __init__(self, root, basedir):
        self._root = Path(root)
        self._basedir = Path(basedir)
        self.texture_extensions = [".tga", ".dds", ".png", ".bmp", ".tex"]
        self.model_extensions = [".e3d", ".t3d"]

    def find_texture_paths(self, rel_path, find_mat=True):
        rel_path = self._normalize_path(rel_path)
        lookups = [
            Path(self._root),
            Path(self._basedir),
            Path(self._root, "textures")
        ]

        extensions = (
            [".mat"] + self.texture_extensions if find_mat 
            else self.texture_extensions
        )

        yield from self._find_paths(rel_path, lookups, extensions)

    def find_model_paths(self, rel_path):
        rel_path = self._normalize_path(rel_path)
        lookups = [
            Path(self._root),
            Path(self._basedir),
            Path(self._root, "models")
        ]

        yield from self._find_paths(rel_path, lookups, self.model_extensions)

    def find_include_paths(self, rel_path):
        rel_path = self._normalize_path(rel_path, trim_ext=False)
        lookups = [
            Path(self._root),
            Path(self._basedir),
            # TODO: Should be more?
        ]

        yield from self._find_paths(rel_path, lookups, [])

    def _find_paths(self, rel_path, lookups, extensions):
        for lookup in lookups:
            full_path = Path(lookup, rel_path)
            for ext in extensions:
                yield str(full_path.with_suffix(ext))

        return

    # TODO: Refactor
    def _normalize_path(self, path, trim_ext=True):
        path = os.path.splitext(path)[0] if trim_ext else path
        path = os.path.normpath(path.replace('\\', '/')).lstrip('/').lower()
        return path