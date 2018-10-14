from io import TextIOWrapper
from typing import Iterator, Tuple, Any

from eu07_tools.io.utils.tokenize import TokenStream


class T3DPropertiesParser:
    """
    This class is part of the T3D loader system and is responsible for
    extracting raw submodel properties associated with their values. 
    """
    # public:
    def parse_properties(self, file: TextIOWrapper) -> Iterator[Tuple[str, Any]]:
        self._token_stream = TokenStream.from_file(file)

        while True:
            token = self._token_stream.get_token()

            if token == "":
                return

            key = token.rstrip(":")

            if key == "include":
                parameters = list(self._token_stream.get_tokens_before("end"))
                value = parameters

            elif key in "Ambient Diffuse Specular":
                value = list(self._token_stream.get_tokens(3))

            elif key == "Transform":
                value = list(self._token_stream.get_tokens(16))

            elif key == "NumVerts":
                # If submodel has NumVerts property, that means we have
                # geometry definition below.
                value = self._token_stream.get_token()
                yield key, value

                num_verts = int(value)
                yield "GEOMETRY", self._parse_geometry(num_verts)
                continue

            elif key in "SelfIllum":
                value = self._token_stream.get_token().lower()
                if value == "true":
                    value = "1"
                elif value == "false":
                    value = "0"

            else:
                value = self._token_stream.get_token()

            yield key, value
             
    @property
    def progress(self) -> float:
        return self._token_stream.progress

    @property
    def current_line_number(self) -> int:
        return self._token_stream.current_line_number

    # internal:
    def _parse_geometry(self, num_total_verts: int):
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

            unit_flag = self._token_stream.get_token()
            vertex_size = 8 if unit_flag == "-1" else 5

            geometry_unit = [
                unit_flag,
                *self._token_stream.get_tokens(vertex_size * unit_size)
            ]
            geometry.append(geometry_unit)

            num_loaded_verts += unit_size

        return geometry




