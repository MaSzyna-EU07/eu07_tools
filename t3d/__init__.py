import warnings

from .input import load, T3DInput
from .output import dump, T3DOutput
from .structures import (
    create_include, create_submodel,
    Element, Include,
    Submodel, MeshSubmodel, FreeSpotLightSubmodel, StarsSubmodel,
    StarsLight
)
from ..utils.structures.mesh_geometry import MeshTriangle