from collections.abc import Iterator
from eu07_tools.utils.input import TokenStream
from eu07_tools.t3d.structures import create_submodel, create_include
from . import type_cast


def load(file):
    inp = T3DInput.from_file(file)
    yield from iter(inp)


class T3DInput(Iterator):
    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __init__(self, file):
        self._fragments_loader = T3DFragmentsLoader.from_file(file)
        self._dict_builder = T3DDictSubmodelBuilder()
        self._datablocks_iter = self._iter_datablocks()

    def __next__(self):
        return next(self._datablocks_iter)

    def _iter_datablocks(self):
        for identifier, value in self._fragments_loader:

            if identifier == "include":
                yield self._load_include(value)
                
            elif identifier == "parent":
                yield self._load_submodel(value)

    def _load_include(self, parameters):
        return create_include(parameters[0])

    def _load_submodel(self, parent_name):
        dct = self._dict_builder.build_from_fragments(self._fragments_loader)

        submodel = create_submodel(dct["type"], dct["name"])
        submodel.parent_name = parent_name
        submodel.anim = dct["anim"]
        submodel.diffuse = dct["diffuse"]
        submodel.selfillum = dct["selfillum"]
        submodel.max_distance = dct["maxdistance"]
        submodel.min_distance = dct["mindistance"]
        submodel.transform = dct["transform"]

        if dct["type"] == "Mesh":
            submodel.ambient = dct["ambient"]
            submodel.specular = dct["specular"]
            submodel.wire = dct["wire"]
            submodel.wire_size = dct["wiresize"]
            submodel.opacity = dct["opacity"]
            submodel.map = dct["map"]

            for unit in dct["geometry"]:
                submodel.add_triangle(unit[1:], unit[0])

        elif dct["type"] == "FreeSpotLight":
            submodel.near_atten_start = dct["nearattenstart"]
            submodel.near_atten_end = dct["nearattenend"]
            submodel.use_near_atten = dct["usenearatten"]
            submodel.far_atten_decay_type = dct["farattendecaytype"]
            submodel.far_decay_radius = dct["fardecayradius"]
            submodel.falloff_angle = dct["falloffangle"]
            submodel.hotspot_angle = dct["hotspotangle"]

        elif dct["type"] == "Stars":
            for unit in dct["geometry"]:
                for vertex in unit[1:]:
                    encoded_color = int(vertex[3])
                    decoded_color = (
                        ((encoded_color) & 0xff) / 255.0,
                        ((encoded_color >> 8) & 0xff) / 255.0,
                        ((encoded_color >> 16) & 0xff) / 255.0
                    )

                    submodel.add_star(vertex[:3], decoded_color)

        return submodel
        

class T3DDictSubmodelBuilder:
    def __init__(self):
        self._NUM_FRAGMENTS_AFTER_TYPE = {
            "Mesh": 15,
            "FreeSpotLight": 14,
            "Stars": 9
        }

    def build_from_fragments(self, fragments_loader):
        dct = {}
        __, dct["type"] = next(fragments_loader)

        num_iterations = self._NUM_FRAGMENTS_AFTER_TYPE[dct["type"]]
        for _ in range(num_iterations):

            identifier, value = next(fragments_loader)
            value = type_cast.cast_fragment_value(identifier, value)
            dct[identifier] = value

        return dct



class T3DFragmentsLoader(Iterator):
    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __init__(self, file):
        self._token_stream = TokenStream.from_file(file)
        self._fragments_iterator = self._iter_fragments()

    def __next__(self):
        return next(self._fragments_iterator)

    def _iter_fragments(self):
        while True:
            token = self._token_stream.get_token()

            if token == "":
                return

            identifier = token.rstrip(":").lower()

            if identifier == "include":
                parameters = list(self._token_stream.get_tokens_before("end"))
                value = parameters

            elif identifier in "ambient diffuse specular":
                value = list(self._token_stream.get_tokens(3))

            elif identifier == "transform":
                value = list(self._token_stream.get_tokens(16))

            elif identifier == "numverts":
                # If submodel has NumVerts property, that means we have
                # geometry definition below.
                value = self._token_stream.get_token()
                yield identifier, value

                num_verts = int(value)
                identifier = "geometry"
                value = self._load_geometry(num_verts)

            elif identifier in "selfillum":
                value = self._token_stream.get_token().lower()
                if value == "true":
                    value = "1"
                elif value == "false":
                    value = "0"

            else:
                value = self._token_stream.get_token()

            yield identifier, value

    # internal:
    def _load_geometry(self, num_total_verts):
        geometry = []
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

            unit_flag = self._token_stream.get_token()
            vertex_size = 8 if unit_flag == "-1" else 5

            vertices = [
                list(self._token_stream.get_tokens(vertex_size)) 
                for _ in range(unit_size)
            ]

            geometry_unit = [unit_flag, *vertices]

            geometry.append(geometry_unit)

        return geometry
