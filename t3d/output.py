import math

from ..utils import TextWriter

def dump(elements, file):
    T3DOutput(file).dump_from_iterable(elements)

class T3DOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)

    def dump_from_iterable(self, elements):
        for element in elements:
            self.dump_element(element)

    def dump_element(self, element):
        if element.element_type == "include":
            parameters = "".join(f"{parameter} " for parameter in element.parameters)
            self._writer.write_string(f"include {element.path} {parameters}end\n")
        elif element.element_type == "submodel":
            self._dump_submodel(element)

    def _dump_submodel(self, submodel):
        self._writer.write_string(f"//{'-' * 81}\n")
        self._write_property("Parent", submodel.parent_name)
        self._write_property("Type", submodel.type)
        self._write_property("Name", submodel.name)
        self._write_property("Anim", submodel.anim)

        if submodel.type == "Mesh":
            self._write_property("Ambient", submodel.ambient_color)
            self._write_property("Diffuse", submodel.diffuse_color)
            self._write_property("Specular", submodel.specular_color)
            self._write_property("SelfIllum", submodel.selfillum)
            self._write_property("Wire", submodel.wire)
            self._write_property("WireSize", submodel.wire_size)
            self._write_property("Opacity", submodel.opacity)
            self._write_property("Map", submodel.map.get_full_reference_path())
            
        elif submodel.type == "FreeSpotLight":
            self._write_property("Diffuse", submodel.diffuse_color)
            self._write_property("SelfIllum", submodel.selfillum)
            self._write_property("NearAttenStart", submodel.near_atten_start)
            self._write_property("NearAttenEnd", submodel.near_atten_end)
            self._write_property("UseNearAtten", submodel.use_near_atten)
            self._write_property("FarAttenDecayType", submodel.far_atten_decay_type)
            self._write_property("FarDecayRadius", submodel.far_decay_radius)
            self._write_property("FalloffAngle", submodel.falloff_angle)
            self._write_property("HotspotAngle", submodel.hotspot_angle)
            if submodel.hotspot_power is not None:
                self._write_property("HotspotPower", submodel.hotspot_power)
            if submodel.radius is not None:
                self._write_property("Radius", submodel.radius)
            if submodel.shade_self is not None:
                self._write_property("ShadeSelf", submodel.shade_self)
            if submodel.cast_shadows is not None:
                self._write_property("CastShadows", submodel.cast_shadows)
            if submodel.soft_falloff is not None:
                self._write_property("SoftFalloff", submodel.soft_falloff)

        elif submodel.type == "Stars":
            self._write_property("Diffuse", submodel.diffuse_color)
            self._write_property("SelfIllum", submodel.selfillum)

        self._write_property("MaxDistance", submodel.max_distance)
        self._write_property("MinDistance", submodel.min_distance)
        # the elements which are parameters of an included file go as they are written in it
        transform = list(submodel.transform)
        for index, token in getattr(submodel, "transform_params", {}).items():
            transform[index] = token
        self._write_property("Transform", transform)

        self._dump_geometry(submodel)


    def _dump_geometry(self, submodel):
        if submodel.type == "Mesh":
            if submodel.geometry.is_empty:
                self._write_property("NumVerts", 0)

            elif submodel.geometry.is_indexed:
                num_indices = len(submodel.geometry.indices)

                self._write_property("NumIndices", num_indices)
                for i in range(num_indices // 3):
                    self._writer.write_floats(submodel.geometry.indices[i*3:i*3+3])
                    self._writer.write_string("\n")

                self._writer.write_string("\n")
                self._write_property("NumVerts", len(submodel.geometry.vertices))
                for vertex in submodel.geometry.vertices:
                    self._writer.write_floats(vertex)
                    self._writer.write_string("\n")
            elif submodel.geometry.is_triangles:
                self._write_property("NumVerts", len(submodel.geometry.vertices))
                for triangle in submodel.geometry.triangles:
                    self._writer.write_int(triangle.smooth)
                    self._writer.write_string("\n")

                    for vertex in triangle.vertices:
                        self._writer.write_floats(vertex)
                        self._writer.write_string("\n")

                    self._writer.write_string("\n")

            else:
                raise ValueError(f"Bad T3D geometry type: {submodel.geometry.type}")

        elif submodel.type == "Stars":
            self._write_property("NumVerts", len(submodel.stars))

            num_groups = math.ceil(len(submodel.stars) / 3) 

            for group_id in range(num_groups):
                self._writer.write_string("1\n")

                stars = submodel.stars[group_id * 3: group_id * 3 + 3]
                for star in stars:
                    self._writer.write_floats(star.location)
                    self._writer.write_floats([star.bin_color, 0])
                    self._writer.write_string("\n")
                
                self._writer.write_string("\n")

    def _write_property(self, key, value):
        self._writer.write_string(f"{key}:")

        key_lower = key.lower()
        if key_lower in "ambient diffuse specular":
            self._writer.write_floats(value)

        elif key_lower in "transform":
            for row in range(4):
                self._writer.write_string("\n\t")
                for element in value[row * 4:row * 4 + 4]:
                    if isinstance(element, str):
                        self._writer.write_string(element)
                    else:
                        self._writer.write_float(element)
            self._writer.write_string("\n")

        elif key_lower in "usenearatten wire":
            self._writer.write_string("true" if value else "false")

        elif key_lower in ("shadeself", "castshadows", "softfalloff"):
            self._writer.write_string("true" if value else "false")

        elif key_lower in "parent name":
            self._writer.write_string(value, is_enquotable=True)

        elif key_lower in "type anim map":
            self._writer.write_string(value)

        elif key_lower in "farattendecaytype numverts":
            self._writer.write_int(value)

        elif key_lower in "selfillum":
            if value == 2.0:
                self._writer.write_string("true")
            elif value == -1:
                self._writer.write_string("false")
            else:
                self._writer.write_float(value)

        else:
            self._writer.write_float(value)

        self._writer.write_string("\n")