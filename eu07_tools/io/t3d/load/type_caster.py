from typing import Sequence, Any

from eu07_tools.io.utils import bool_from_string

class T3DTypeCaster:
    """ Class for providing correct variable type for T3D properties """
    def __init__(self):
        self._cast_funcs = {
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
            self._self_illum_from_string: [
                "selfillum"
            ],
            self._floats_from_strings: [
                "ambient",
                "diffuse",
                "specular",
                "transform"
            ],
            self._geometry_from_strings: [
                "geometry"
            ],
        }

    def cast_property_value(self, key: str, value: Any):
        cast_func = self._get_cast_func(key)
        new_value = cast_func(value)
           
        return new_value

    def _get_cast_func(self, key: str):
        for cast_func, properties in self._cast_funcs.items():
            if key in properties:
                return cast_func
        
        # If no caster was found, value type should be string
        return str

    def _self_illum_from_string(self, self_illum: str) -> float:
        if self_illum == "true":
            value = 1.0
        elif self_illum == "false":
            value = 0.0
        else:
            value = float(self_illum)

        return value

    def _floats_from_strings(self, values: Sequence[str]) -> Sequence[float]:
        return [float(value) for value in values]

    def _geometry_from_strings(self, string_geometry):
        geometry = []
        for string_geometry_unit in string_geometry:

            geometry_unit = []

            geometry_unit.append(int(string_geometry_unit[0]))
            for vertex in string_geometry_unit[1:]:
                geometry_unit.append(
                    self._floats_from_strings(vertex)
                )

            geometry.append(geometry_unit)

        return geometry