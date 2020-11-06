from .structures import VectorUV, VectorXY, VectorXYZ, Vertex3D, ColorRGB, ColorRGBA, FactorySequence, OwnedFactorySequence
from .asset_searcher import AssetSearcher
from .input import TextScanner, BinaryScanner
from .output import BinaryWriter, TextWriter
from .model_convert import e3d_to_t3d, t3d_to_e3d

from pathlib import Path

def find_asset_root(filepath):
    root = Path("")
    filepath = Path(filepath).resolve()

    for part in filepath.parts:
        # TODO: More dirs?
        if part in "models dynamic textures scripts sounds shaders scenery":
            break
        root /= part

    root = root.resolve()
    root_found = root != filepath
    if root_found:
        return str(root)
    else:
        raise ValueError(f"Can't find EU07 root for {filepath}")


def shorten_asset_path(filepath):
    filepath = Path(filepath).resolve()
    root = Path(find_asset_root(filepath))

    # TODO: Shorten model path, scenery path etc
    shortpath = filepath.relative_to(root).with_suffix("")
    if "textures" in shortpath.parts:
        shortpath = shortpath.relative_to("textures")

    return str(shortpath)

def switch_coordinate_system(vector):
    return [-vector[0], vector[2], vector[1]]