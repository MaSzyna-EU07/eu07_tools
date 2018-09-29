

_MESH_VALIDATION_QUEUE = [
    "parent", "type", "name", "anim", 
    "ambient", "diffuse", "specular", "selfillum" "wire", 
    "wiresize", "opacity", "map", "maxdistance",
    "mindistance", "transform", "numverts", "geometry"
]
_FREESPOT_VALIDATION_QUEUE = [
    "parent", "type", "name", "anim", 
    "selfillum", "diffuse", "nearattenstart", "nearattenend",
    "usenearatten", "farattendecaytype", "fardecayradius",
    "falloffangle", "hotspotangle",
    "mindistance", "transform"
]
_STARS_VALIDATION_QUEUE = [
    "parent", "type", "name", "anim", 
    "selfillum", "diffuse",
    "mindistance", "transform", "numverts", "geometry"
]

class T3DSyntaxValidator:
    def __init__(self):
        self._validation_modes = {
            "mesh": _MESH_VALIDATION_QUEUE,
            "freespotlight": _FREESPOT_VALIDATION_QUEUE,
            "stars": _STARS_VALIDATION_QUEUE,
        }
        self._validation_mode = None
        self._ALLOWED_SUBMODEL_TYPES = "mesh stars freespotlight" 

    def set_validation_mode(self, mode: str):
        self._validation_mode = self._validation_modes[mode]


    def is_property_valid(self, key: str, value: str):
        expected_key = ... # pop from queue
        if key == expected_key:
            if key == "type":
                return self._validate_type(value):
        else:
            raise
        

    def _validate_type(self, type_name: str) -> bool:
        return type_name in self._ALLOWED_SUBMODEL_TYPES
        
        