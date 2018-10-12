from __future__ import annotations
import collections
from typing import Any, Iterable, Sequence


class EntitySet(collections.abc.Set):
    def __init__(self, items: Iterable[Any]):
        self._items = set(items)

    def __contains__(self, item: Any):
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def add(self, item: Any):
        self._items.add(item)

    def discard(self, item: Any):
        self._items.discard(item)

    def __str__(self):
        str_items = " ".join(
            str(item) for item in self._items
        )
        return f"[ {str_items} ]" 


class Texture:
    def __init__(self, path: str, traits: str = ""):
        self.path: str = path
        self.use_vertical_wrap: bool = ("s" in traits)
        self.use_horizontal_wrap: bool = ("t" in traits)
        self.use_sharpening: bool = ("#" in traits)

    def __str__(self):
        traits = ":"
        traits += "t" if self.use_vertical_wrap else ""
        traits += "s" if self.use_horizontal_wrap else ""
        traits += "#" if self.use_sharpening else ""

        has_traits = traits != ":"

        return f"{self.path}{traits if has_traits else ''}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({str(self)})"
        )








class Bezier3D:
    pass



