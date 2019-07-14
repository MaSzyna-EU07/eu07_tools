class SCNNodeTrianglesLoader:
        def _load_node_triangles(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangles(name)
        )

    def _load_node_triangle_strip(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangleStrip(name)
        )

    def _load_node_triangle_fan(self, name):
        return self._generic_load_triangles(
            scnstruct.SCNNodeTriangleFan(name)
        )


    def _generic_load_triangles(self, node):
        token = self._scanner.read_string()
        map_ = token

        if token == "material":
            self._scanner.read_string()
            ambient = list(self._scanner.read_floats(3))
            self._scanner.read_string()
            diffuse = list(self._scanner.read_floats(3))
            self._scanner.read_string()
            specular = list(self._scanner.read_floats(3))
            self._scanner.read_string()

            node.material = scnstruct.SCNTrianglesMaterial(ambient, diffuse, specular)
            map_ = self._scanner.read_string()
            
        node.map = map_

        # TODO: Optimize
        tokens = self._scanner.get_strings_before("endtri")
        tokens = [token for token in tokens if token != "end"]
        num_verts = len(tokens) // 8

        for vi in range(num_verts):
            node.vertices.new(
                [float(x) for x in tokens[8 * vi : 8 * vi + 8]]
            )

        return node