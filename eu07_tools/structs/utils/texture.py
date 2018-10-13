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