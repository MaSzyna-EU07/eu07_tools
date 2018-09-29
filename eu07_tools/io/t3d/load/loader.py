from io import TextIOWrapper
from typing import Iterator, Union

from eu07_tools.structs.t3d.submodel import T3DSubmodel
from .parser import T3DPropertiesParser
from .type_caster import T3DTypeCaster
from .build_submodel import build_submodel
from eu07_tools.structs.utils import IncludedFile


class T3DLoader:
    def __init__(self):
        self._NUMS_MAX_PROPERTIES = {
            "mesh": 17,
            "freespotlight": 16,
            "stars": 11
        }

        self._parser = T3DPropertiesParser()
        self._type_caster = T3DTypeCaster()
        self._properties_iter = None

    # TODO: Validation
    def load_from_file(self, file: TextIOWrapper, validate: bool=False) -> Iterator[Union[IncludedFile, T3DSubmodel]]:
        self._properties_iter = self._parser.parse_properties(file)

        while True:
            try:
                key, value = next(self._properties_iter)
            except StopIteration:
                return None

            if key == "include":
                path, *parameters = value
                yield IncludedFile(path, *parameters)
            elif key == "parent":
                submodel = self._load_submodel(parent_name=value)
                yield submodel
            else:
                if validate:
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
        submodel_dict["parent"] = parent_name
        __, type_ = next(self._properties_iter)
        submodel_dict["type"] = type_

        # TODO: Type validation
        num_max_properties = self._NUMS_MAX_PROPERTIES[type_.lower()]

        while len(submodel_dict) < num_max_properties:
            key, value = next(self._properties_iter)
            casted_value = self._type_caster.cast_property_value(key, value)
            submodel_dict[key] = casted_value

        return build_submodel(submodel_dict)
    

        
        
        