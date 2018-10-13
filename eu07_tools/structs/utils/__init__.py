from .vectors import VectorXYZ, VectorUV, ColorRGB
from .vertex_3d import Vertex3D

# class EntitySet(collections.abc.Set):
#     def __init__(self, items: Iterable[Any]):
#         self._items = set(items)

#     def __contains__(self, item: Any):
#         return item in self._items

#     def __iter__(self):
#         return iter(self._items)

#     def __len__(self):
#         return len(self._items)

#     def add(self, item: Any):
#         self._items.add(item)

#     def discard(self, item: Any):
#         self._items.discard(item)

#     def __str__(self):
#         str_items = " ".join(
#             str(item) for item in self._items
#         )
#         return f"[ {str_items} ]" 