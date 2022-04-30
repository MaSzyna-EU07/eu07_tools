import enum

from eu07_tools.utils import Vertex3D


class MeshGeometry:
    class Type(enum.Enum):
        TRIANGLES = 0
        ORDERED = 1
        INDEXED = 2

    def __init__(self):
        self.vertices = []
        self.indices = []
        self.triangles = []

        self.type = MeshGeometry.Type.TRIANGLES

    # TODO: if-typed code should be polymorphic
    def as_triangles(self):
        new_geo = MeshGeometry()
        new_geo.type = MeshGeometry.Type.TRIANGLES

        if self.type == MeshGeometry.Type.TRIANGLES:
            return self

        elif self.type == MeshGeometry.Type.ORDERED:

            triangle_vertices = []

            for vertex_idx, vertex in self.vertices:
                triangle_vertices.append(vertex)
                if (vertex_idx + 1) % 3 == 0:
                    triangle = MeshTriangle(triangle_vertices, smooth=-1)
                    new_geo.triangles.append(triangle)

        elif self.type == MeshGeometry.Type.INDEXED:

            num_indices = len(self.indices)
            for i in range(num_indices // 3):
                indices = self.indices[i * 3:i * 3 + 3]
                triangle_vertices = [self.vertices[idx] for idx in indices]
                triangle = MeshTriangle(triangle_vertices, smooth=-1)
                new_geo.triangles.append(triangle)

        return new_geo

    def as_ordered(self):
        new_geo = MeshGeometry()
        new_geo.type = MeshGeometry.Type.ORDERED

        if self.type == MeshGeometry.Type.ORDERED:
            return self

        elif self.type == MeshGeometry.Type.TRIANGLES:
            new_geo = MeshGeometry()
            new_geo.type = MeshGeometry.Type.ORDERED

            for triangle in self.triangles:
                for vertex in triangle:
                    new_geo.vertices.append(vertex)

        elif self.type == MeshGeometry.Type.INDEXED:
            for vertex_index in self.indices:
                new_geo.vertices.append(self.vertices[vertex_index])

        return new_geo

    def as_indexed(self):
        new_geo = MeshGeometry()
        new_geo.type = MeshGeometry.Type.INDEXED

        if self.type == MeshGeometry.Type.INDEXED:
            return self

        elif self.type == MeshGeometry.Type.TRIANGLES:
            pass

        elif self.type == MeshGeometry.Type.ORDERED:
            pass

    def calc_smooth_groups_normals(self):
        if self.type != MeshGeometry.Type.TRIANGLES:
            raise Exception("Can't calculate smooth groups normals for indexed or ordered geometry!")

        calc = SmoothGroupsNormalCalculator()
        calc.run(self)


class MeshTriangle:
    def __init__(self, vertices, smooth=0):
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth = -1 if any(
            vertex.use_normal for vertex in self.vertices
        ) else smooth

    @property
    def is_degenerate(self):
        edge1 = self.vertices[1].location - self.vertices[0].location
        edge2 = self.vertices[2].location - self.vertices[0].location

        return edge1.cross(edge2).length_squared == 0

    def normal_calculated(self):
        edge01 = self.vertices[0].location - self.vertices[1].location
        edge02 = self.vertices[0].location - self.vertices[2].location

        normal = edge01.cross(edge02)
        if normal.length_squared > 0:
            normal.normalize()
        else:
            normal.zero()

        return normal


class VertexStorageSectored:
    def __init__(self):
        self._vertices_sectors = {}
        self.vertices = []
        self.original_indices = []
        self.num_verts = 0

    def push(self, vertex):
        sector = self.get_sector(vertex.location)

        self.vertices.append(vertex)

        vertex_index = self.num_verts
        sector[vertex_index] = vertex
        self.num_verts += 1

        return vertex_index

    def find(self, vertex):
        sector = self.get_sector(vertex.location)
        for vertex_index, vertex_candidate in sector.items():
            if vertex_candidate.location.compare_equality(vertex.location):
                return vertex_index

        raise KeyError(f"{vertex} not exists in given sector {sector}")

    def __getitem__(self, index):
        return self.vertices[index]

    def __iter__(self):
        return iter(self.vertices)

    def get_sector(self, vector):
        sector_key = tuple(round(v, ndigits=2) for v in vector)
        sector = self._vertices_sectors.get(sector_key)

        if not sector:
            sector = self._vertices_sectors[sector_key] = {}

        return sector


class SmoothGroupsNormalCalculator:
    def run(self, geometry):
        self.verts_storage = VertexStorageSectored()
        self.tris_normals = []
        self.smooth_groups = []
        triangles = []

        # Pushing vertices to lookup-optimized storage and calculating triangle normals
        for triangle_index, triangle in enumerate(geometry):
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

            triangle.smooth = -1
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
