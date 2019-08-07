import warnings

try:
    from .input import load
except ImportError:
    warnings.warn("You are using non-dev eu07_tools version. t3d.load function is not present.")
from .output import dump
from .structures import (
    create_include, create_submodel,
    Element, Include,
    Submodel, MeshSubmodel, FreeSpotLightSubmodel, StarsSubmodel,
    MeshTriangle, StarsLight
)