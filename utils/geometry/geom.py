import abc
import enum

from ...utils import FactorySequence, Vertex3D
from .smooth_normals_calc import SmoothGroupsNormalCalculator


class Geometry:
    class Type(enum.Enum):
        TRIANGLES = 0
        ORDERED = 1
        INDEXED = 2

    def __init__(self, type_=0):
        self._data = GeometryDataTriangles()

        if type_ == Geometry.Type.ORDERED:
            self._data = GeometryDataOrdered()
        elif type_ == Geometry.Type.INDEXED:
            self._data = GeometryDataIndexed()

    @property
    def type(self):
        return self._data.type

    @property
    def vertices(self):
        return self._data.vertices

    @vertices.setter
    def vertices(self, vertices):
        self._data.vertices = vertices

    @property
    def indices(self):
        return self._data.indices

    @indices.setter
    def indices(self, indices):
        self._data.indices = indices

    @property
    def triangles(self):
        return self._data.triangles

    @triangles.setter
    def triangles(self, triangles):
        self._data.triangles = triangles

    @property
    def is_triangles(self):
        return self.type == Geometry.Type.TRIANGLES

    @property
    def is_ordered(self):
        return self.type == Geometry.Type.ORDERED

    @property
    def is_indexed(self):
        return self.type == Geometry.Type.INDEXED

    def to_triangles(self):
        self._data.to_triangles()
        self._data = GeometryDataTriangles(self._data)

    def to_ordered(self):
        self._data.to_ordered()
        self._data = GeometryDataOrdered(self._data)

    def to_indexed(self):
        self._data.to_indexed()
        self._data = GeometryDataIndexed(self._data)

    @property
    def is_empty(self):
        if self.is_triangles:
            return len(self.triangles) == 0
        elif self.is_indexed:
            return len(self.indices) + len(self.vertices) == 0
        elif self.is_ordered:
            return len(self.vertices) == 0

    def calc_smooth_groups_normals(self):
        if self.is_triangles:
            raise ValueError("Can't calculate smooth groups normals for indexed or ordered mesh_data!")

        calc = SmoothGroupsNormalCalculator()
        calc.run(self)


class GeometryData(abc.ABC):
    def __init__(self, old_data=None):
        self._vertices = FactorySequence(Vertex3D)
        self._indices = FactorySequence(int)
        self._triangles = FactorySequence(MeshTriangle)

        if old_data:
            self._vertices = old_data.vertices
            self._indices = old_data.indices
            self._triangles = old_data.triangles


    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices.clear()
        for vertex in vertices:
            self._vertices.append(vertex)

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, indices):
        self._indices.clear()
        for index in indices:
            self._indices.append(index)

    @property
    def triangles(self):
        return self._triangles

    @triangles.setter
    def triangles(self, triangles):
        self._triangles.clear()
        for triangle in triangles:
            self._triangles.append(triangle)

    @abc.abstractmethod
    def to_triangles(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_ordered(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_indexed(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def type(self):
        raise NotImplementedError()


class GeometryDataTriangles(GeometryData):
    def __init__(self, old_data=None):
        super().__init__(old_data)

    def to_triangles(self):
        pass

    def to_ordered(self):
        for triangle in self._triangles:
            for vertex in triangle:
                self._vertices.append(vertex)

        self._triangles.clear()

    def to_indexed(self):
        pass

    @property
    def type(self):
        return Geometry.Type.TRIANGLES


class GeometryDataOrdered(GeometryData):
    def __init__(self, old_data=None):
        super().__init__(old_data)

    def to_triangles(self):
        num_triangles = len(self._vertices) // 3

        for triangle_idx in range(num_triangles):
            tri_verts = self._vertices[triangle_idx * 3: triangle_idx * 3 + 3]
            triangle = MeshTriangle(tri_verts, smooth=-1)
            self._triangles.append(triangle)

        self._vertices.clear()

    def to_ordered(self):
        pass

    def to_indexed(self):
        # TODO: Make indexing
        pass

    @property
    def type(self):
        return Geometry.Type.ORDERED


class GeometryDataIndexed(GeometryData):
    def __init__(self, old_data=None):
        super().__init__(old_data)

    def to_triangles(self):
        num_indices = len(self._indices)
        for i in range(num_indices // 3):
            indices = self._indices[i * 3:i * 3 + 3]
            triangle_vertices = [self._vertices[idx] for idx in indices]
            triangle = MeshTriangle(triangle_vertices, smooth=-1)
            self._triangles.append(triangle)

        self._indices.clear()
        self._vertices.clear()

    def to_ordered(self):
        for vertex_index in self._indices:
            self._vertices.append(self._vertices[vertex_index])

        self._indices.clear()
        self._triangles.clear()

    def to_indexed(self):
        pass

    @property
    def type(self):
        return Geometry.Type.INDEXED


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