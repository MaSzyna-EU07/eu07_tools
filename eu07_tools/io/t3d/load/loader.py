from io import TextIOWrapper
from typing import Iterator, Tuple, Any

from eu07_tools.structs.t3d.submodel import T3DSubmodel
from .parser import T3DPropertiesParser
from .type_caster import T3DTypeCaster


class T3DLoader:
    """
    Class for loading T3D text model files.
    """
    def __init__(self):
        self._NUMS_MAX_PROPERTIES = {
            "Mesh": 17,
            "FreeSpotLight": 16,
            "Stars": 11
        }

        self._parser = T3DPropertiesParser()
        self._type_caster = T3DTypeCaster()
        self._properties_iter = None

    # TODO: Validation
    def load_from_file(self, file: TextIOWrapper) -> Iterator[Tuple[str, Any]]:
        """ Read given file and yield tuple with entry identifier and entry datablock. """
        self._properties_iter = self._parser.parse_properties(file)

        while True:
            try:
                key, value = next(self._properties_iter)
            except StopIteration:
                return None

            if key == "include":
                yield "include", list(value)

            elif key == "Parent":
                submodel_dict = self._load_submodel(parent_name=value)
                yield "submodel", submodel_dict

            else:
                raise SyntaxError(
                    f"Unexpected token \"{key}\"" 
                    f"in file {file.name}" 
                    f"at line {self._parser.current_line_number}"
                )

    @property
    def progress(self) -> float:
        return self._parser.progress

    def _load_submodel(self, parent_name: str):
        submodel_dict = {}
        submodel_dict["Parent"] = parent_name
        __, type_ = next(self._properties_iter)
        submodel_dict["Type"] = type_

        # TODO: Type validation
        num_max_properties = self._NUMS_MAX_PROPERTIES[type_]

        while len(submodel_dict) < num_max_properties:
            key, value = next(self._properties_iter)
            casted_value = self._type_caster.cast_property_value(key, value)
            submodel_dict[key] = casted_value

        return submodel_dict
    

        
        
        