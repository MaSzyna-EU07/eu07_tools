from collections.abc import Iterator
import eu07_tools.t3d
from eu07_tools.utils import TextScanner


def load(file):
    return T3DInput(file).load()


class T3DInput:
    def __init__(self, file):
        self._scanner = TextScanner.from_file(file)
        
    def load(self):
        while True:
            token = self._scanner.read_string().lower().rstrip(":")

            if token == "":
                return
            elif token == "parent":
                parent_name = self._scanner.read_string()
                yield self._load_submodel(parent_name)
            elif token == "include":
                path, *parameters = self._scanner.get_strings_before("end")
                yield eu07_tools.t3d.create_include(path, parameters)

    def _load_submodel(self, parent_name):
        type_ = self._read_property()
        name = self._read_property()

        submodel = eu07_tools.t3d.create_submodel(type_, name)

        submodel.parent_name = parent_name
        submodel.anim = self._read_property()

        if submodel.type == "Mesh":
            submodel.ambient_color = self._read_property()
            submodel.diffuse_color = self._read_property()
            submodel.specular_color = self._read_property()
            submodel.selfillum = self._read_property()
            submodel.wire = self._read_property()
            submodel.wire_size = self._read_property()
            submodel.opacity = self._read_property()
            submodel.map = self._read_property()

        elif submodel.type == "FreeSpotLight":
            submodel.diffuse_color = self._read_property()
            submodel.selfillum = self._read_property()
            submodel.near_atten_start = self._read_property()
            submodel.near_atten_end = self._read_property()
            submodel.use_near_atten = self._read_property()
            submodel.far_atten_decay_type = self._read_property()
            submodel.far_decay_radius = self._read_property()
            submodel.falloff_angle = self._read_property()
            submodel.hotspot_angle = self._read_property()

        elif submodel.type == "Stars":
            submodel.diffuse_color = self._read_property()
            submodel.selfillum = self._read_property()

        submodel.max_distance = self._read_property()
        submodel.min_distance = self._read_property()
        submodel.transform = self._read_property()

        if submodel.type in "Stars Mesh":
            self._load_geometry(submodel)

        return submodel

    def _load_geometry(self, submodel):
        num_total_verts = self._read_property()
        
        num_loaded_verts = 0
        MAX_UNIT_SIZE = 3

        if num_total_verts % MAX_UNIT_SIZE == 0:
            LAST_UNIT_SIZE = MAX_UNIT_SIZE
        else:
            LAST_UNIT_SIZE = num_total_verts % MAX_UNIT_SIZE

        while num_loaded_verts < num_total_verts:
            is_last_unit = (num_loaded_verts + MAX_UNIT_SIZE >= num_total_verts)
            unit_size = LAST_UNIT_SIZE if is_last_unit else MAX_UNIT_SIZE
            num_loaded_verts += unit_size

            unit_flag = self._scanner.read_int()

            vertex_size = 8 if unit_flag == -1 else 5
            vertices = [self._scanner.read_floats(vertex_size) for _ in range(unit_size)]

            if submodel.type == "Mesh":
                submodel.triangles.new(vertices, unit_flag)
            elif submodel.type == "Stars":
                for vertex in vertices:
                    submodel.stars.new(vertex[:3], vertex[3])

    def _read_property(self):
        propname = self._scanner.read_string().lower().rstrip(":")

        if propname in ("ambient", "diffuse", "specular"):
            value = self._scanner.read_floats(3)

        elif propname in ("transform",):
            value = self._scanner.read_floats(16)

        elif propname in ("usenearatten", "wire"):
            value = (self._scanner.read_string() == "true")

        elif propname in ("selfillum",):
            token = self._scanner.read_string()
            if token == "false":
                value = 0
            elif token == "true":
                value = 1
            else:
                value = float(token)

        elif propname in ("numverts", "farattendecaytype"):
            value = self._scanner.read_int()

        elif propname in ("parent", "name", "map", "anim", "type"):
            value = self._scanner.read_string()

        else:
            value = self._scanner.read_float()

        return value

    

            
