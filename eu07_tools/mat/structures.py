from eu07_tools.utils import VectorXY


def create_mat_mapping():
    return MATMapping()

# TODO: Collections.abc subclass
class MATMapping:
    def __init__(self):
        self._items = {}

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        if key == "size":
            self._items["size"] = VectorXY(value)
        else:
            self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def get(self, key, value):
        return self._items.get(key, value)

    def update(self, dict2):
        self._items.update(dict2)

    def clear(self):
        self._items.clear()

    def pop(self, key, default=None):
        return self._items.pop(key, default)

    def popitem(self):
        return self._items.popitem()

    def setdefault(self, key, default_value=None):
        self._items.setdefault(key, default_value)

