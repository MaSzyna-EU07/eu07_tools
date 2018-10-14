from typing import Sequence, Any

from eu07_tools.io.utils import bool_from_string

class T3DTypeCaster:
    """ Class for providing correct variable type for T3D properties """
    def __init__(self):
        self._cast_funcs = {
            int: [
                "FarAttenDecayType",
                "NumVerts"
            ],
            float: [
                "MaxDistance",
                "MinDistance",
                "WireSize",
                "Opacity",
                "NearAttenStart",
                "NearAttenEnd",
                "FarDecayRadius",
                "FalloffAngle",
                "HotspotAngle",
            ],
            bool_from_string: [
                "Wire",
                "UseNearAtten"
            ],
            self._self_illum_from_string: [
                "SelfIllum"
            ],
            self._floats_from_strings: [
                "Ambient",
                "Diffuse",
                "Specular",
                "Transform"
            ],
            self._geometry_from_strings: [
                "GEOMETRY"
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

    def _geometry_from_strings(self, geometry):
        casted_geometry = []
        for unit in geometry:
            casted_unit = self._floats_from_strings(unit)
            casted_unit[0] = int(casted_unit[0])
            casted_geometry.append(casted_unit)

        return casted_geometry