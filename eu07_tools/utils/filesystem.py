from pathlib import Path
import os

class EU07Filesystem:
    def __init__(self, root):
        self._root = Path(root)
        self.material_extensions = [".mat", ".tga", ".dds", ".png", ".bmp", ".tex"]
        self.model_extensions = [".e3d", ".t3d"]

    # TODO: Remove redundancy
    # TODO: trimextension,
    def find_material(self, filepath, basedir):
        filepath = os.path.splitext(filepath.lstrip("/").lstrip("\\").lower())[0]
        lookups = [
            Path(self._root),
            Path(basedir),
            Path(self._root, "textures")
        ]

        for lookup in lookups:
            for ext in self.material_extensions:
                fullpath = Path(lookup, filepath + ext)
                print(fullpath)
                if fullpath.exists():
                    return str(fullpath)

        return ""

    def find_model(self, filepath, basedir):
        lookups = [
            Path(self._root),
            Path(basedir),
            Path(self._root, "models")
        ]

        for lookup in lookups:
            for ext in self.model_extensions:
                fullpath = Path(lookup, filepath + ext)
                if fullpath.exists():
                    return str(fullpath)

        return ""

    def find_included_file(self, filepath, basedir):
        lookups = [
            Path(self._root),
            Path(basedir),
            Path(self._root, "models")
        ]

        for lookup in lookups:
            fullpath = Path(lookup, filepath)
            if fullpath.exists():
                return str(fullpath)

        return ""

    # TODO: Refactor
    def _normalize_path(self, path, trim_ext=True):
        path = os.path.splitext(path)[0] if trim_ext else path
        path = os.path.normpath(path.replace('\\', '/')).lstrip('/').lower()
        return path
