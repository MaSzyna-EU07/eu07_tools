from .format import *

DEFAULT_NEWLINE = "\r\n"
DEFAULT_ENCODING = "windows-1250"

class T3DDumper:
    def __init__(self, file, newline=DEFAULT_NEWLINE, encoding=DEFAULT_ENCODING):
        self.file = file
        self.newline = newline
        self.encoding = encoding
        self._latest_entry_type = ""
        self._dict = ""

    # Public:

    def dump_submodel_object(self, submodel: T3DSubmodel):
        pass

    def dump_submodel_dict(self, dict_: Dict[str, Any]):
        self._dict = dict_
        self._write_property_from_dict("Parent")
        self._write_property_from_dict("Type")
        self._write_property_from_dict("Name")
        self._write_property_from_dict("Anim")
        
        if dict_["Type"] == "Mesh":
            self._write_property_from_dict("Ambient")
            self._write_property_from_dict("Diffuse")
            self._write_property_from_dict("Specular")
            self._write_property_from_dict("SelfIllum")
            self._write_property_from_dict("Wire")
            self._write_property_from_dict("WireSize")
            self._write_property_from_dict("Opacity")
            self._write_property_from_dict("Map")
        elif
        
        self._write_property_from_dict("MaxDistance")
        self._write_property_from_dict("MinDistance")
        self._write_property_from_dict("Transform")

        if not "Geometry" in dict_:
            dict_["Geometry"] = []
        self._write_property_from_dict("Geometry")

        self._latest_entry_type = "submodel"

    def dump_include(self, params: Iterable[object]):
        self.file.write(
            f"include {params} end{self.newline}"
        )
        
        if "submodel" in self._latest_entry_type:
            self.file.write(self.newline)

        self._latest_entry_type = "include"

    # Internal:

    def _write_property_from_dict(self, key: str):
        value = self._dict.get(key)
        key_lower = key.lower()
        if key_lower in "ambient diffuse specular":
            value = format_sequence(value)
        elif key_lower in "transform":
            value = format_matrix(value)
        elif key_lower in "usenearatten wire":
            value = format_bool(value)
        elif key_lower in "geometry":
            self._write_geometry(value)
        # HACK: It's easier to type all keys of string properties
        # than typing keys of all numeric properties...
        elif key_lower in "parent type name anim map":
            pass
        else:
            value = format_number(value)
 
        self.file.write(
            f"{key}: {value}" + "{newline}"
            .format(newline=self.newline)
            .encode(self.encoding)
        )

    def _write_geometry(self, geometry):
        self.file.write(
            (self.newline * 2).join(
                format_geometry_unit(unit)
                for unit in geometry
            )
        )
        self.file.write(self.newline)

    
    