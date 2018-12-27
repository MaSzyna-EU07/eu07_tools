from eu07_tools.utils.input import bool_from_string

def cast_fragment_value(key, value):
    cast_func = _get_cast_func(key)
    new_value = cast_func(value)
        
    return new_value

def _get_cast_func(key: str):
    for cast_func, properties in _func_to_keys_map.items():
        if key in properties:
            return cast_func

    # If no caster was found, value type should be string
    return str

def _selfillum_from_string(selfillum: str) -> float:
    if selfillum == "true":
        value = 1.0
    elif selfillum == "false":
        value = 0.0
    else:
        value = float(selfillum)

    return value

def _floats_from_strings(values):
    return [float(value) for value in values]

def _geometry_from_strings(geometry):
    casted_geometry = []
    for unit in geometry:
        casted_vertices = [_floats_from_strings(v) for v in unit[1:]]
        casted_unit = [int(unit[0]), *casted_vertices]
        casted_geometry.append(casted_unit)

    return casted_geometry

_func_to_keys_map = {
    int: [
        "farattendecaytype",
        "numverts"
    ],
    float: [
        "maxdistance",
        "mindistance",
        "wiresize",
        "opacity",
        "nearattenstart",
        "nearattenend",
        "fardecayradius",
        "falloffangle",
        "hotspotangle",
    ],
    bool_from_string: [
        "wire",
        "usenearatten"
    ],
    _selfillum_from_string: [
        "selfillum"
    ],
    _floats_from_strings: [
        "ambient",
        "diffuse",
        "specular",
        "transform"
    ],
    _geometry_from_strings: [
        "geometry"
    ],
}

