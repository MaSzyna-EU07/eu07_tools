from .structures import VectorUV, VectorXY, VectorXYZ, Vertex3D, ColorRGB
from .asset_searcher import AssetSearcher
from .input import TokenStream

from pathlib import Path

def find_root(filepath):
    root = Path("")
    filepath = Path(filepath)

    for part in filepath.parts:
        # TODO: More dirs?
        if part in "models dynamic textures scripts sounds shaders":
            break
        root /= part

    root_found = (not root.samefile(filepath))
    if root_found:
        return root
    else:
        raise ValueError(f"Can't find EU07 root for {filepath}")