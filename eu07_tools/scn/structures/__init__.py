from . import directives
from . import nodes
 
_typename_to_class = {
    "atmo": directives.Atmo,
    "camera": directives.Camera,
    "config": directives.Config,
    "description": directives.Description,
    "event": directives.Event,
    "firstinit": directives.FirstInit,
    "include": directives.Include,
    "light": directives.Light,
    "lua": directives.Lua,
    "origin": directives.Origin,
    "endorigin": directives.EndOrigin,
    "rotate": directives.Rotate,
    "sky": directives.Sky,
    "time": directives.Time,
    "trainset":directives.Trainset,
    "endtrainset": directives.EndTrainset,

    "node:dynamic": nodes.NodeDynamic,
    "node:eventlauncher": nodes.NodeEventlauncher,
    "node:lines": nodes.NodeLines,
    "node:memcell": nodes.NodeMemcell,
    "node:model": nodes.NodeModel,
    "node:sound": nodes.NodeSound,
    "node:track": nodes.NodeTrack,
    "node:traction": nodes.NodeTraction,
    "node:tractionpowersource": nodes.NodeTractionPowerSource,
    "node:triangles": nodes.NodeTriangles,
}

def create_element(typename, name=""):
    cls = _typename_to_class.get(typename)
    if not cls:
        raise ValueError("Unknown SCN element type name")
    
    try:
        # Node take name as constructor parameter
        return cls(name)
    except TypeError:
        # Directive take no parameters
        return cls()


