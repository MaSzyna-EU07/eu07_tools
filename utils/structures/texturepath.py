class TexturePath:
    REPLACABLESKINS_VALUES = {"-1", "-2", "-3", "-4", "replacableskin"}

    def __init__(self, path=""):
        self.path = path
        self.traits = TexturePathTraits()
        self.use_script = False
        self.script = TexturePathScript()


    @classmethod
    def from_string(cls, string):
        instance = cls()
        instance.set_from_string(string)

        return instance

    def set_from_string(self, string):
        if string in self.REPLACABLESKINS_VALUES:
            string = "-1" if string == "replacableskin" else string

        elif string.startswith(self.script.STARTTAG):
            self.script.set_from_string(string)

        # Parse traits
        parts = string.split(":")
        self.path = parts[0]

        has_traits = (len(parts) == 2)
        if has_traits:
            self.traits.set_from_string(parts[1])

    def as_string(self):
        if self.is_replacableskin:
            return self.path
        elif self.is_script_call:
            return self.script.as_string()
        else:
            return f"{self.path}{self.traits.as_string()}"

    @property
    def is_replacableskin(self):
        return self.path in self.REPLACABLESKINS_VALUES

    @property
    def is_script_call(self):
        return self.use_script

    @property
    def is_path(self):
        return (
            not self.is_replacableskin() and
            not self.is_script_call
        )

    def __str__(self):
        return self.as_string()


    @property
    def disable_wrap_s(self):
        return self.traits.disable_wrap_s

    @disable_wrap_s.setter
    def disable_wrap_s(self, state):
        self.traits.disable_wrap_s = state

    @property
    def disable_wrap_t(self):
        return self.traits.disable_wrap_t

    @disable_wrap_t.setter
    def disable_wrap_t(self, state):
        self.traits.disable_wrap_t = state

    @property
    def use_sharpen(self):
        return self.traits.use_sharpen

    @use_sharpen.setter
    def use_sharpen(self, state):
        self.traits.use_sharpen = state

    @property
    def script_path(self):
        return self.script.path

    @script_path.setter
    def script_path(self, script_path):
        self.script.path = script_path

    @property
    def script_params(self):
        return self.script.params

    @script_params.setter
    def script_params(self, script_params):
        self.script.params = script_params


class TexturePathTraits:
    def __init__(self):
        self.disable_wrap_s = False
        self.disable_wrap_t = False
        self.use_sharpen = False

    def set_from_string(self, string):
        self.disable_wrap_s = "s" in string
        self.disable_wrap_t = "t" in string
        self.use_sharpen = "#" in string

    def as_string(self):
        traits_string = ":"
        traits_string += "s" if self.disable_wrap_s else ""
        traits_string += "t" if self.disable_wrap_t else ""
        traits_string += "#" if self.use_sharpen else ""

        return traits_string if traits_string != ":" else ""


class TexturePathScript:
    STARTTAG = "make:"
    PARAMS_STARTTAG = "?"
    PARAMS_SEPARATOR = "&"
    KEY_VALUE_SEPARATOR = "="

    def __init__(self):
        self.path = ""
        self.params = {}

    def set_from_string(self, string):
        parts = (
            string.lstrip(self.STARTTAG)
            .split(self.PARAMS_STARTTAG)
        )

        if len(parts) == 2:
            self.path, params_string = parts

            self.params = {}

            for ps in params_string.split(self.PARAMS_SEPARATOR):
                k, v = ps.split(self.PARAMS_KEY_VALUE_SEPARATOR)
                self.params[k] = v

        else:
            self.path = parts[0]
            self.params = {}

    def as_string(self):
        params_string = self.PARAMS_SEPARATOR.join(
            f"{k}{self.PARAMS_KEY_VALUE_SEPARATOR}{v}"
            for k, v in self.params.items()
        )

        return f"{self.STARTTAG}{self.script_path}{self.PARAMS_STARTTAG}{params_string}"