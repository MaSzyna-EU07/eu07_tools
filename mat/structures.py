from eu07_tools.utils import VectorXY
import collections.abc
import enum

from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS


def create_mapping():
    return Mapping()

class Mapping(collections.abc.MutableMapping):
    def __init__(self):
        self._items = {}

    @classmethod
    def from_dict(cls, d):
        map_ = create_mapping()
        for k, v in d.items():
            map_[k] = v

        return map_

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        if key == "size":
            self._items["size"] = VectorXY(value)
        elif "texture" in key:
            self._items[key] = Texture(value)
        else:
            self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

class Texture:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.value_type = (
            "TEXTURE_SET" if isinstance(value, list)
            else "TEXTURE_PATH"
        )
        self._value = value

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"type={self.value_type} "
            f"value={self.value}>"
        )

    def __str__(self):
        if self.value_type == "TEXTURE_SET":
            return "[ " + " ".join(self._value) + " ]"
        else:
            return self.value


class TextureReference:
    class Type(enum.Enum):
        PATH = 0
        SKIN_INDEX = 1
        GENERATED = 2


    def __init__(self, string):
        self.type = TextureReference.Type.PATH

        self._resource_path = ""

        self.use_wrap_s = False
        self.use_wrap_t = False
        self.use_sharpen = False

        self.skin_index = 0

        self.generated_params = {}

        self.feed(string)

    def get_full_reference_path(self):
        return str(self)

    def __str__(self):
        if self.type == TextureReference.Type.PATH:
            traits_str = self.get_traits_str()
            traits_str = f":{traits_str}" if traits_str else traits_str

            return f"{self._resource_path}{traits_str}"
        elif self.type == TextureReference.Type.SKIN_INDEX:
            return str(self.skin_index)
        elif self.type == TextureReference.Type.GENERATED:
            params_str = ""
            for k, v in self.generated_params:
                params_str += f"{k}={v}&"

            params_str = params_str[:-1] if params_str else ""

            return f"make:{self._resource_path}?{params_str}"

    def feed(self, data):
        if isinstance(data, TextureReference):
            self.type = data.type
            self.resource_path = data.resource_path
            self.use_wrap_s = data.use_wrap_s
            self.use_wrap_t = data.use_wrap_t
            self.use_sharpen = data.use_sharpen
            self.skin_index = data.skin_index
            self.generated_params = data.generated_params

        elif data.startswith("make:"):
            self.type = TextureReference.Type.GENERATED

            data = data[6:]

            splitted = data.split("?")
            self._resource_path = splitted[0]
            if len(splitted) == 2:
                params_strings = splitted[1].split("&")
                for ps in params_strings:
                    key, value = ps.split("=")
                    self.generated_params[key] = value

        elif data.startswith("-"):
            self.type = TextureReference.Type.SKIN_INDEX

            self.skin_index = int(data)
        else:
            self.type = TextureReference.Type.PATH

            splitted = data.split(":")
            self._resource_path = splitted[0]
            if len(splitted) == 2:
                self.set_traits_from_str(splitted[1])

    def get_traits_str(self):
        string = ""
        string += "s" if self.use_wrap_s else ""
        string += "t" if self.use_wrap_t else ""
        string += "#" if self.use_sharpen else ""

        return string

    def set_traits_from_str(self, string):
        self.use_wrap_s = ("s" in string)
        self.use_wrap_t = ("t" in string)
        self.use_sharpen = ("#" in string)

    @property
    def resource_path(self):
        return self._resource_path

    @resource_path.setter
    def resource_path(self, resource_path):
        self._resource_path = str(resource_path)

    @property
    def has_problend(self):
        return self.type == TextureReference.Type.PATH and self._resource_path.startswith("@")

    @property
    def is_none(self):
        return self._resource_path == "none"

    @property
    def is_skin(self):
        return self._resource_path.startswith("-") or self._resource_path == "replacableskin"



