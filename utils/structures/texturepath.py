REPLACABLESKINS_VALUES = {"-1", "-2", "-3", "-4", "replacableskin"}

class TexturePath:
    def __init__(self, path):
        self._path = "none"
        self.path = path # Call property to set flags
        self.use_wrap_s = True
        self.use_wrap_t = True
        self.use_sharpen = False

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

            self.use_wrap_s = "s" not in traits
            self.use_wrap_t = "t" not in traits
            self.use_sharpen = "#" in traits

    @property
    def path_with_traits(self):
        if self.is_replacableskin:
            return self._path

        traits_string = ""
        traits_string += "s" if not self.use_wrap_s else ""
        traits_string += "t" if not self.use_wrap_t else ""
        traits_string += "#" if self.use_sharpen else ""

        return f"{self._path}:{traits_string}" if traits_string else self._path

    @property
    def is_replacableskin(self):
        return self._path in REPLACABLESKINS_VALUES

    def __str__(self):
        return self.path_with_traits()