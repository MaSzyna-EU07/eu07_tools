from collections.abc import Iterator
from .structures import create_include, create_submodel
from ..utils import TextScanner, has_parameters, substitute_parameters
from ..utils.geometry import Geometry



# optional true/false entries of FreeSpotLight and the attributes of FreeSpotLightSubmodel they go to
LIGHT_FLAGS = {
    "shadeself": "shade_self",
    "castshadows": "cast_shadows",
    "softfalloff": "soft_falloff",
    "lightonly": "light_only",
}


def load(file, parameters=None):
    """ Parameters: the values the include of the file gives its parameters (p1), (p2) ..., which are put in place of them
    in every token as the simulator does. The names and the transform matrices keep what is written in the file as well:
    name_template, parent_template and transform_params of the submodels, raw_parameters of the includes """
    return T3DInput(file, parameters).load()


class T3DInput:
    def __init__(self, file, parameters=None):
        self._parameters = list(parameters) if parameters else []
        self._scanner = TextScanner.from_file(file, parameters=self._parameters)

    def _substituted(self, raw):
        return substitute_parameters(raw, self._parameters)

    def _template(self, raw):
        return raw if has_parameters(raw) else None
        
    def load(self):
        while True:
            token = self._scanner.read_string().lower().rstrip(":")

            if token == "":
                return
            elif token == "parent":
                raw_parent = self._scanner.read_raw_string()
                try:
                    yield self._load_submodel(raw_parent)
                except ValueError as e:
                    raise ValueError(f"Bad T3D syntax in line: {self._scanner.line_number}")
            elif token == "include":
                raw = []
                while True:
                    item = self._scanner.read_raw_string()
                    if item == "" or item == "end":
                        break
                    raw.append(item)
                if raw:
                    path, *parameters = [self._substituted(item) for item in raw]
                    include = create_include(path, parameters)
                    # as written in the file: parameters of this file passed on stay parameters
                    include.raw_parameters = raw[1:]
                    yield include

    def _load_submodel(self, raw_parent):
        type_ = self._read_property()
        if self._scanner.read_string().lower().rstrip(":") != "name":
            raise ValueError("Expected Name")
        raw_name = self._scanner.read_raw_string()

        submodel = create_submodel(type_, self._substituted(raw_name))

        submodel.parent_name = self._substituted(raw_parent)
        # the names as written in the file, when they hold parameters
        submodel.name_template = self._template(raw_name)
        submodel.parent_template = self._template(raw_parent)
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
            # optional entries in any order, which the simulator takes right after HotspotAngle
            while True:
                token = self._scanner.read_string()
                key = token.lower().rstrip(":")
                if key == "hotspotpower":
                    submodel.hotspot_power = self._scanner.read_float()
                elif key == "radius":
                    submodel.radius = self._scanner.read_float()
                elif key in LIGHT_FLAGS:
                    setattr(submodel, LIGHT_FLAGS[key], self._scanner.read_string().lower() in ("true", "yes", "1"))
                else:
                    self._scanner.put_back(token)
                    break

        elif submodel.type == "Stars":
            submodel.diffuse_color = self._read_property()
            submodel.selfillum = self._read_property()

        submodel.max_distance = self._read_property()
        submodel.min_distance = self._read_property()
        self._read_transform(submodel)

        if submodel.type in "Stars Mesh":
            self._load_geometry(submodel)

        return submodel

    def _load_geometry(self, submodel):
        token = self._scanner.read_string().lower()
        # TODO: Too much if-type, get rid of this

        if submodel.type == "Mesh":
            geo = submodel.geometry

        if "numindices" in token:
            geo.to_indexed()

            num_indices = self._scanner.read_int()

            for i in range(num_indices):
                geo.indices.append(self._scanner.read_int())

            num_verts = self._read_property()
            for i in range(num_verts):
                vertex = geo.vertices.new(self._scanner.read_floats(12))

        elif "numverts" in token:
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
                    geo.triangles.new(vertices, unit_flag)
                elif submodel.type == "Stars":
                    for vertex in vertices:
                        submodel.stars.new(vertex[:3], vertex[3])


    def _read_transform(self, submodel):
        """ Transform matrix, whose elements may be parameters of an included file """
        propname = self._scanner.read_string().lower().rstrip(":")
        if propname != "transform":
            raise ValueError(f"Expected Transform, got {propname}")
        submodel.transform = []
        submodel.transform_params = {}
        for index in range(16):
            token = self._scanner.read_raw_string()
            if has_parameters(token):
                submodel.transform_params[index] = token
                value = substitute_parameters(token, self._parameters)
            else:
                value = token
            try:
                submodel.transform.append(float(value))
            except ValueError:
                # a parameter without a value of a number: the matrix holds 0 in its place
                submodel.transform.append(0.0)

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
                value = -1.0
            elif token == "true":
                value = 2.0
            else:
                value = float(token)

        elif propname in ("numverts", "farattendecaytype"):
            value = self._scanner.read_int()

        elif propname in ("parent", "name", "map", "anim", "type"):
            value = self._scanner.read_string()

        elif propname == "opacity":
            value = self._scanner.read_float()
            if value > 1:
                value = value / 100

        else:
            value = self._scanner.read_float()

        return value




