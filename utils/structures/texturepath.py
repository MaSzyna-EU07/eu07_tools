REPLACABLESKINS_VALUES = {"-1", "-2", "-3", "-4", "replacableskin"}

class TexturePath:
    def __init__(self, value):
        self.disable_wrap_s = False
        self.disable_wrap_t = False
        self.use_sharpen = False
        self.path = value

        if isinstance(value, TexturePath):
            self.path = value.path_with_traits()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if path == "replacableskin":
            path = "-1"

        parts = path.split(":")
        self._path = parts[0]
        if len(parts) == 2:
            traits = parts[1]

            self.disable_wrap_s = "s" in traits
            self.disable_wrap_t = "t" in traits
            self.use_sharpen = "#" in traits

    @property
    def path_with_traits(self):
        if self.is_replacableskin:
            return self._path

        ts = self.traits_suffix

        return f"{self._path}{ts}" if ts else self._path

    @property
    def traits_suffix(self):
        traits_string = ":"
        traits_string += "s" if self.disable_wrap_s else ""
        traits_string += "t" if self.disable_wrap_t else ""
        traits_string += "#" if self.use_sharpen else ""

        return traits_string if traits_string != ":" else ""

    @property
    def is_replacableskin(self):
        return self._path in REPLACABLESKINS_VALUES

    def __str__(self):
        return self.path_with_traits()