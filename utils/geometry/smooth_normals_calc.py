from .verts_storage import VertexStorageSectored


class SmoothGroupsNormalCalculator:
    def run(self, geometry):
        self.verts_storage = VertexStorageSectored()
        self.tris_normals = []
        self.smooth_groups = []
        triangles = []

        # Pushing vertices to lookup-optimized storage and calculating triangle normals
        for triangle_index, triangle in enumerate(geometry.triangles):
            if triangle.is_degenerate:
                continue

            triangles.append(triangle)
            normal = triangle.normal_calculated()
            self.tris_normals.append(normal)

            self.smooth_groups.append(triangle.smooth)

            for vertex in triangle.vertices:
                self.verts_storage.push(vertex)

        # Calculating per-face vertex normals
        self.precalculated_normals = {}
        for triangle_index, triangle in enumerate(triangles):
            triangle_normal = self.tris_normals[triangle_index]

            for local_vert_index, vertex in enumerate(triangle.vertices):
                vertex_index = triangle_index * 3 + local_vert_index

                try:
                    vertex.normal = self.precalculated_normals[vertex_index]
                except KeyError:
                    if triangle.smooth == -1:
                       if vertex.normal.length_squared > 0:
                           vertex.normal.normalize()

                    elif triangle.smooth == 0:
                        vertex.normal = triangle_normal

                    else:
                        vertex.normal, shared_indices = self._calc_smooth_group_normal(
                            vertex, self.tris_normals[triangle_index], triangle.smooth
                        )

                        if vertex.normal.length_squared > 0:
                            vertex.normal.normalize()
                        else:
                            vertex.normal = triangle_normal

                        for shared_index in shared_indices:
                            self.precalculated_normals[shared_index] = vertex.normal

                    self.precalculated_normals[vertex_index] = vertex.normal

            triangle.smooth = -1


    def _calc_smooth_group_normal(self, vertex, initial_normal, smooth_group):
        sector = self.verts_storage.get_sector(vertex.location)

        normal = initial_normal

        shared_indices = set()
        for sc_vertex_index, sc_vertex in sector.items():
            if not sc_vertex.location.compare_equality(vertex.location):
                continue
            triangle_index = sc_vertex_index // 3
            sc_vertex_smooth_group = self.smooth_groups[triangle_index]

            if sc_vertex_smooth_group & smooth_group:
                adjacent_normal = self.tris_normals[triangle_index]
                if not adjacent_normal.compare_equality(normal):
                    normal = normal + adjacent_normal
                    shared_indices.add(sc_vertex_index)

        return normal.normalized, shared_indices