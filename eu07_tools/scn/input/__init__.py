from collections.abc import Iterator
import functools

from eu07_tools.utils.input import TokenStream
from eu07_tools.scn.structures import (
    SCNNodeTriangles, SCNNodeTriangleFan, SCNNodeTriangleStrip,
    SCNTrianglesMaterial
)

class SCNIterativeLoader(Iterator):
    def __init__(self, file):
        self._token_stream = TokenStream.from_file(file)
        self._iterator = self._load()

        self._element_loaders = {
            "node": self._load_node,
        }

        self._node_loaders = {
            "triangles": self._load_node_triangles,
            "triangle_strip": self._load_node_triangle_strip,
            "triangle_fan": self._load_node_triangle_fan
        }

        self._get_token = self._token_stream.get_token
        self._get_tokens = self._token_stream.get_tokens
        self._get_tokens_before = self._token_stream.get_tokens_before

    @classmethod
    def from_file(cls, file):
        return cls(file)

    def __next__(self):
        return next(self._iterator)

    def _load(self):
        while True:
            token = self._token_stream.get_token().lower()

            if token == "":
                return

            load_element = self._element_loaders.get(token)

            if load_element:
                yield load_element()


    def _load_node(self):
        max_distance = float(self._get_token())
        min_distance = float(self._get_token())
        name, subtype = self._get_tokens(2)

        load_node = self._node_loaders.get(subtype)

        if load_node:
            node = load_node(name)

        node.max_distance = max_distance
        node.min_distance = min_distance

        return node

    def _load_node_triangles(self, name):
        return self._help_load_triangles(SCNNodeTriangles(name))

    def _load_node_triangle_strip(self, name):
        return self._help_load_triangles(SCNNodeTriangleStrip(name))

    def _load_node_triangle_fan(self, name):
        return self._help_load_triangles(SCNNodeTriangleFan(name))


    def _help_load_triangles(self, node):
        token = self._get_token()
        map_ = token

        if token == "material":
            self._get_token()
            ambient = list(self._get_typed_tokens(3, float))
            self._get_token()
            diffuse = list(self._get_typed_tokens(3, float))
            self._get_token()
            specular = list(self._get_typed_tokens(3, float))
            self._get_token()

            node.material = SCNTrianglesMaterial(ambient, diffuse, specular)
            map_ = self._get_token()
            
        node.map = map_

        # TODO: Optimize
        tokens = self._get_tokens_before("endtri")
        tokens = [token for token in tokens if token != "end"]
        num_verts = len(tokens) // 8

        for vi in range(num_verts):
            node.add_vertex(
                [float(x) for x in tokens[8 * vi : 8 * vi + 8]]
            )

        return node


    def _get_typed_tokens(self, count, type_):
        return (type_(self._get_token()) for _ in range(count))
