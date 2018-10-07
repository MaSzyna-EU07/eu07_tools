from __future__ import annotations
from .submodel import T3DSubmodel


class T3DFreeSpotLightSubmodel(T3DSubmodel):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "FreeSpotLight"
        self.near_atten_start: float = 40.0
        self.near_atten_end: float = 0.0
        self.use_near_atten: bool = False
        self.far_atten_decay_type: int = 1
        self.far_decay_radius: float = 45.0
        self.falloff_angle: float = 45.0
        self.hotspot_angle: float = 45.0