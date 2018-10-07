from .mesh import T3DMeshSubmodel
from .stars import T3DStarsSubmodel
from .freespotlight import T3DFreeSpotLightSubmodel
from .submodel import T3DSubmodel


def create_submodel(name: str, type_: str) -> T3DSubmodel:
    """ Create named T3DSubmodel instance """
    type_lowered = type_.lower()
    if type_lowered == "mesh":
        return T3DMeshSubmodel(name)
    elif type_lowered == "freespotlight":
        return T3DFreeSpotLightSubmodel(name)
    elif type_lowered == "stars":
        return T3DStarsSubmodel(name)

    raise ValueError(f"Bad T3D submodel type: {type_}") 