class Material:
    def __init__(self):
        self.textures = {}
        self.variants: Dict[str, Material] = {}
        self.params = {}
        self.shader_path: str = None
        self.opacity: float = None
        self.selfillum: float = None
        self.size: Vector2 = None

