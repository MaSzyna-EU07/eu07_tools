import math

from eu07_tools.utils import TextWriter

def dump(elements, file):
    T3DOutput(file).dump(elements)

class T3DOutput:
    def __init__(self, file):
        self._writer = TextWriter(file)

    def dump(self, elements):
        for e in elements:
            if e.element_type == "include":
                self._writer.write_string(f"include {e.path} end\n")
            elif e.element_type == "submodel":
                self._dump_submodel(e)
                

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
            self._write_property("Map", submodel.map)
            
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

        elif submodel.type == "Stars":
            self._write_property("Diffuse", submodel.diffuse_color)
            self._write_property("SelfIllum", submodel.selfillum)

            num_groups = math.ceil(len(submodel.stars) / 3) 

            for group_id in range(num_groups):
                self._writer.write_string("1\n")

                stars = submodel.stars[group_id * 3: group_id * 3 + 3]
                for star in stars:
                    self._writer.write_floats(star.location)
                    self._writer.write_floats([star.bin_color, 0])
                    self._writer.write_string("\n")
                
                self._writer.write_string("\n")

        self._write_property("MaxDistance", submodel.max_distance)
        self._write_property("MinDistance", submodel.min_distance)
        self._write_property("Transform", submodel.transform)

        if submodel.type == "Mesh":
            for triangle in submodel.triangles:
                self._writer.write_int(triangle.smooth)
                self._writer.write_string("\n")

                for vertex in triangle.vertices:
                    self._writer.write_floats(vertex)
                    self._writer.write_string("\n")

                self._writer.write_string("\n")

    def _write_property(self, key, value):
        self._writer.write_string(f"{key}:")

        key_lower = key.lower()
        if key_lower in "ambient diffuse specular":
            self._writer.write_floats(value)

        elif key_lower in "transform":
            self._writer.write_string("\n\t")
            self._writer.write_floats(value[:4])
            self._writer.write_string("\n\t")
            self._writer.write_floats(value[4:8])
            self._writer.write_string("\n\t")
            self._writer.write_floats(value[8:12])
            self._writer.write_string("\n\t")
            self._writer.write_floats(value[12:])
            self._writer.write_string("\n")

        elif key_lower in "usenearatten wire":
            self._writer.write_string("true" if value else "false")

        elif key_lower in "parent name":
            if " " in value:
                self._writer.write_string(f"\"{value}\"")
            else:
                self._writer.write_string(value)

        elif key_lower in "type anim map numverts":
            self._writer.write_string(value)

        else:
            self._writer.write_int(value)

        self._writer.write_string("\n")