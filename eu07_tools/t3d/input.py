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
                path, __ = self._scanner.read_strings(2)
                yield eu07_tools.t3d.create_include(path)

    def _load_submodel(self, parent_name):
        __, type_ = self._scanner.read_strings(2)
        __, name = self._scanner.read_strings(2)

        submodel = eu07_tools.t3d.create_submodel(type_, name)

        submodel.parent_name = parent_name
        __, submodel.anim = self._scanner.read_strings(2)

        if submodel.type == "Mesh":
            self._scanner.read_string()
            submodel.ambient_color = self._scanner.read_floats(3)

            self._scanner.read_string()
            submodel.diffuse_color = self._scanner.read_floats(3)

            self._scanner.read_string()
            submodel.specular_color = self._scanner.read_floats(3)

            submodel.selfillum = self._read_selfillum()

            __, wire = self._scanner.read_strings(2)
            submodel.wire = (wire == "true") 

            self._scanner.read_string()
            submodel.wire_size = self._scanner.read_float()

            self._scanner.read_string()
            submodel.opacity = self._scanner.read_float()

            __, submodel.map = self._scanner.read_strings(2)

        elif submodel.type == "FreeSpotLight":
            self._scanner.read_string()
            submodel.diffuse_color = self._scanner.read_floats(3)

            submodel.selfillum = self._read_selfillum()

            self._scanner.read_string()
            submodel.near_atten_start = self._scanner.read_float()
            
            self._scanner.read_string()
            submodel.near_atten_end = self._scanner.read_float()

            __, use_near_atten = self._scanner.read_strings(2)
            submodel.use_near_atten = (use_near_atten == "true") 
            
            self._scanner.read_string()
            submodel.far_atten_decay_type = self._scanner.read_int()

            self._scanner.read_string()
            submodel.far_decay_radius = self._scanner.read_float()

            self._scanner.read_string()
            submodel.falloff_angle = self._scanner.read_float()
           
            self._scanner.read_string()
            submodel.hotspot_angle = self._scanner.read_float()

        elif submodel.type == "Stars":
            self._scanner.read_string()
            submodel.diffuse_color = self._scanner.read_floats(3)

            submodel.selfillum = self._read_selfillum()

        self._scanner.read_string()
        submodel.max_distance = self._scanner.read_float()

        self._scanner.read_string()
        submodel.min_distance = self._scanner.read_float()

        self._scanner.read_string()
        submodel.transform = self._scanner.read_floats(16)

        if submodel.type in "Stars Mesh":
            self._load_geometry(submodel)

        return submodel

    def _read_selfillum(self):
        __, value = self._scanner.read_strings(2)
        if value == "false":
            return 0
        elif value == "true":
            return 1
        else:
            return value

    def _load_geometry(self, submodel):
        self._scanner.read_string()
        num_total_verts = self._scanner.read_int()
        
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

            
