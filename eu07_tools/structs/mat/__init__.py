from typing import Dict, Union, Set

from eu07_tools.structs.utils import Vector2, Texture, EntitySet

class Material:
    def __init__(self):
        self.textures: Dict[str, Union[Texture, EntitySet]] = {}
        self.variants: Dict[str, Material] = {
            "spring": None,
            "summer": None,
            "autumn": None,
            "winter": None,
            "clear": None,
            "cloud": None,
            "rain": None,
            "snow": None,
        }
        self.shader_path: str = None
        self.opacity: float = None
        self.selfillum: float = None
        self.size: Vector2 = None

    @classmethod
    def from_file(self, file):
        pass

    def save_to_file(self, file):
        pass

    def __str__(self):
        pass
