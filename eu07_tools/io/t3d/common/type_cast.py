""" 
Here are some utils for casting datatypes of T3D properties.
"""

_PROPERTY_TYPES = {
    "FLOAT": set(
        "selfillum",
        "maxdistance",
        "mindistance",
        "wiresize",
        "opacity",
        "nearattenstart",
        "nearattenend",
        "fardecayradius",
        "falloffangle",
        "hotspotangle"
    ),
    "STRING": set(
        "parent",
        "type",
        "name",
        "anim",
        "map",
    ),
    "FLOAT_SEQ": set(
        "ambient",
        "diffuse",
        "specular",
        "transform"
    ),
    "INT": set(
        "numverts",
        "farattendecaytype",
    ),
    "BOOL": set(
        "wire",
        "usenearatten"
    ),
    "GEOMETRY": set(
        "geometry"
    )
}

def type_from_string(key: str, value: str):
    datatype = _get_property_datatype(key)

    if datatype in "FLOAT":
        return float(value)
    elif datatype in "FLOAT_SEQ":
        return [float(num) for num in value]
    elif datatype in "INT":
        return int(value)
    elif datatype in "BOOL":
        return value in "true"
    elif datatype in "GEOMETRY":
        return _geometry_from_string(value)
        

def type_to_string(key: str, value: object):
    datatype = _get_property_datatype(key)

    if datatype in "STRING":
        return value
    elif datatype in "FLOAT INT":
        return str(value)
    elif datatype in "FLOAT_SEQ":
        return " ".join(str(num) for num in value)
    elif datatype in "BOOL":
        return str(value).lower()


def _get_property_datatype(key: str) -> str:
    for datatype in _PROPERTY_TYPES:
        if key in datatype:
            return datatype


def _geometry_from_string(string_geometry):
    geometry = []
    for string_geometry_unit in string_geometry:

        geometry_unit = [int(string_geometry_unit[0])]
        geometry_unit += [
            [float(num) for num in vertex] 
            for vertex in string_geometry_unit[1:]
        ]
        geometry.append(geometry_unit)

    return geometry


