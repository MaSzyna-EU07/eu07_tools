from __future__ import annotations
from typing import Iterable, Sequence

from .submodel import T3DSubmodel
from eu07_tools.structs.utils import ColorRGB, Vertex3D

class T3DMeshSubmodel(T3DSubmodel):
    def __init__(self, name: str):
        super().__init__(name)   
        self.type = "Mesh"
        self._ambient: ColorRGB = ColorRGB((255, 255, 255)) 
        self._specular: ColorRGB = ColorRGB((255, 255, 255))
        self.wire: bool = False
        self.wire_size: float = 1.0
        self.opacity: float = 100.0
        self.map = "none"
        self._triangles: Sequence[T3DTriangle] = []

    @property
    def ambient(self) -> ColorRGB:
        return self._ambient

    @ambient.setter
    def ambient(self, ambient: Iterable[float]):
        self._ambient = ColorRGB(ambient)

    @property
    def specular(self) -> ColorRGB:
        return self._specular

    @specular.setter
    def specular(self, specular: Iterable[float]):
        self._specular = ColorRGB(specular)

    @property
    def num_verts(self) -> int:
        return len(self._triangles) * 3

    def add_triangle(self, vertices: Iterable[Iterable[float]], smooth: int=0):
        """ Add new triangle with specified vertices and smooth mask """
        self._triangles.append(
            T3DTriangle(vertices, smooth)
        )

    def remove_triangle(self, triangle: T3DTriangle):
        """ Remove specified triangle from mesh """
        self._triangles.remove(triangle)

    @property
    def triangles(self) -> Sequence[T3DTriangle]:
        return tuple(self._triangles)


class T3DTriangle:
    def __init__(self, vertices: Iterable[Iterable[float]], smooth: int=0):
        self.vertices = tuple(
            Vertex3D(vertex) for vertex in vertices
        )

        self.smooth: int = -1 if any(
            vertex.has_normal for vertex in self.vertices
        ) else smooth

