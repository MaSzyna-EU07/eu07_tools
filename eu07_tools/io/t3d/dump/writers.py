import abc
from .format import (
    format_bool, format_geometry_unit, format_matrix, format_number, 
    format_sequence
)


def get_writer(type_: str) -> SubmodelWriter:
    type_lowered = type_.lower()
    if type_lowered == "mesh":
        return MeshSubmodelWriter()
    elif type_lowered = "freespotlight":
        return FreeSpotLightSubmodelWriter()
    elif type_lowered = "stars":
        return StarsSubmodelWriter()

    raise ValueError(f"Illegal T3D submodel type: {type_}")


class SubmodelWriter(abc.ABC):
    # public:
    def write_submodel(self, submodel: T3DSubmodel, file):
        """ Write submodel object to given file """

        self._write_separator()
        self._write_property("Parent", submodel.parent_name)
        self._write_property("Type", submodel.type)
        self._write_property("Name", submodel.name)
        self._write_property("Anim", submodel.anim)
        
        self._write_specific_properties(submodel)

        self._write_property("MaxDistance", submodel.max_distance)
        self._write_property("MinDistance", submodel.min_distance)
        self._write_property("Transform", submodel.transform)

        self._write_geometry()


    # internal:
    @abc.abstractmethod
    def _write_specific_properties(self, submodel: T3DSubmodel):
        raise NotImplementedError()

    @abc.abstractmethod
    def _write_geometry(self, submodel: T3DSubmodel):
        raise NotImplementedError()

    def _write_property(self, key: str, value: Any):
        key_lower = key.lower()
        if key_lower in "ambient diffuse specular":
            value = format_sequence(value)
        elif key_lower in "transform":
            value = format_matrix(value)
        elif key_lower in "usenearatten wire":
            value = format_bool(value)
        # HACK: It's easier to type all keys of string properties
        # than typing keys of all numeric properties...
        elif key_lower in "parent type name anim map":
            pass
        else:
            value = format_number(value)

        self._file.write(
            f"{key}: {value}{self._newline}"
        )

    def _write_separator(self, length: int=81):
        self._file.write(
            f"//{"-" * length}{self._newline}"
        )
        

class MeshSubmodelWriter(SubmodelWriter):
    def __init__(self, file, newline: str):
        super().__init__(file, newline)

    # internal, overriden:
    def _write_specific_properties(self, submodel: T3DSubmodel):
        self._write_property("Ambient", submodel.ambient)
        self._write_property("Diffuse", submodel.diffuse)
        self._write_property("Specular", submodel.specular)
        self._write_property("SelfIllum", submodel.self_illum)
        self._write_property("Wire", submodel.wire)
        self._write_property("WireSize", submodel.wire_size)
        self._write_property("Opacity", submodel.opacity)
        self._write_property("Map", submodel.map)

    def _write_geometry(self, submodel: T3DSubmodel):
        for triangle in submodel.triangles:
            unit = [triangle.smooth, *triangle.vertices]

            self._file.write(
                format_geometry_unit(unit)
            )

class FreeSpotLightSubmodelWriter(SubmodelWriter):
    # internal, overriden:
    def _write_specific_properties(self, submodel: T3DSubmodel):
        self._write_property("Diffuse", submodel.diffuse)
        self._write_property("SelfIllum", submodel.self_illum)
        self._write_property("NearAttenStart", submodel.near_atten_start)
        self._write_property("NearAttenEnd", submodel.near_atten_end)
        self._write_property("UseNearAtten", submodel.use_near_atten)
        self._write_property("FarAttenDecayType", submodel.far_atten_decay_type)
        self._write_property("FarDecayRadius", submodel.far_decay_radius)
        self._write_property("FalloffAngle", submodel.falloff_angle)
        self._write_property("HotspotAngle", submodel.hotspot_angle)

    def _write_geometry(self, submodel: T3DSubmodel):
        self._file.write(self._newline)


class StarsSubmodelWriter(SubmodelWriter):
    # internal, overriden:
    def _write_specific_properties(self, submodel: T3DSubmodel):
        self._write_property("Diffuse", submodel.diffuse)
        self._write_property("SelfIllum", submodel.self_illum)

    def _write_geometry(self, submodel: T3DSubmodel):
        MAX_GROUP_SIZE = 3
        num_groups = len(submodel.stars) // MAX_GROUP_SIZE

        for group_idx in range(num_groups):
            slice_start = group_idx * MAX_GROUP_SIZE
            slice_end = slice_start + MAX_GROUP_SIZE
            group = [slice_start, slice_end]

            star_lists = []
            for star in group:
    
                color = (
                    (int(star.color[2] * 255) << 16) | 
                    (int(star.color[1] * 255) << 8) | 
                    (int(star.color[0] * 255)
                )

                star_lists.append(
                    [star.position, color, 0]
                )

            unit = [1, *star_lists]
            

            self._file.write(
                format_geometry_unit(unit)
            )



    

    