from . import directives
from . import nodes
from . import events
 
_typename_to_class = {
    "atmo": directives.Atmo,
    "camera": directives.Camera,
    "config": directives.Config,
    "description": directives.Description,
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

    "event:addvalues": events.EventAddvalues,
    "event:copyvalues": events.EventCopyvalues,
    "event:getvalues": events.EventGetvalues,
    "event:logvalues": events.EventLogvalues,
    "event:putvalues": events.EventPutvalues,
    "event:updatevalues": events.EventUpdatevalues,
    "event:animation": events.EventAnimation,
    "event:lights": events.EventLights,
    "event:trackvel": events.EventTrackvel,
    "event:visible": events.EventVisible,
    "event:voltage": events.EventVoltage,
    "event:whois": events.EventWhois,
    "event:friction": events.EventFriction,
    "event:multiple": events.EventMultiple,
    "event:switch": events.EventSwitch,
    "event:sound": events.EventSound,
    "event:disable": events.EventDisable,
    "event:dynvel": events.EventDynvel,
    "event:message": events.EventMessage,
    "event:texture": events.EventTexture,
}

def create_element(typename, name="none"):
    cls = _typename_to_class.get(typename.lower())
    if not cls:
        raise ValueError(f"Unknown SCN element type name: {typename.lower()}")
    
    try:
        # Node and event takes name as constructor parameter
        return cls(name)
    except TypeError:
        # Directive takes no parameters
        return cls()


