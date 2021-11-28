from .structures import VectorUV, VectorXY, VectorXYZ, Vertex3D, ColorRGB, ColorRGBA, FactorySequence, OwnedFactorySequence
from .asset_searcher import AssetSearcher
from .input import TextScanner, BinaryScanner,Tokenizer
from .output import BinaryWriter, TextWriter
from .model_convert import e3d_to_t3d, t3d_to_e3d

from pathlib import Path

class Value:
    def __init__(self, value):
        # moze byc parametr w stringu
        # i moze byc konkret wartosc
        pass


def lower_filepath_name(filepath):
    filepath = Path(filepath)
    return str(Path(filepath.parent, filepath.name.lower()))


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
    if "models" in shortpath.parts:
        shortpath = shortpath.relative_to("models")
    if "textures" in shortpath.parts:
        shortpath = shortpath.relative_to("textures")
    if "sounds" in shortpath.parts:
        shortpath = shortpath.relative_to("sounds")

    return str(shortpath)

def swizzle_coords(vector):
    return [-vector[0], vector[2], vector[1]]
