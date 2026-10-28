from .structures import VectorUV, VectorXY, VectorXYZ, Vertex3D, ColorRGB, ColorRGBA, FactorySequence, OwnedFactorySequence
from .asset_searcher import AssetSearcher
from .input import TextScanner, BinaryScanner,Tokenizer
from .output import BinaryWriter, TextWriter
from .model_convert import e3d_to_t3d, t3d_to_e3d

from pathlib import Path
import re

# a parameter of an included file, (p1), (p2) ...
PARAMETER_PATTERN = re.compile(r"\(p(\d+)\)", re.IGNORECASE)


def has_parameters(token):
    """ Whether the token holds a parameter of an included file, (pN) """
    return PARAMETER_PATTERN.search(token) is not None


def substitute_parameters(token, parameters):
    """ The token with its parameters (pN) replaced by the values the include gives them, as the simulator does: a
    parameter the include doesn't give becomes "none". Without any parameters the token stays as it is """
    if not parameters:
        return token

    def replace(match):
        index = int(match.group(1))
        return str(parameters[index - 1]) if 1 <= index <= len(parameters) else "none"

    return PARAMETER_PATTERN.sub(replace, token)

class Value:
    def __init__(self, value):
        # moze byc parametr w stringu
        # i moze byc konkret wartosc
        pass


def lower_filepath_name(filepath):
    filepath = Path(filepath)
    return str(Path(filepath.parent, filepath.name.lower()))

def enquote_if_whitespace(name):
    if " " in name:
        name = f"\"{name}\""

    return name

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

    try:
        root = Path(find_asset_root(filepath))
    except:
        return str(filepath.stem)

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
