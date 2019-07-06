class FactoryContainer:
    def __init__(self, cls):
        self.cls = cls
        self._items = []

    def new(self, *args):
        instance = self.cls(args)
        self._items.append(instance)
        return instance

    def remove(self, instance):
        self._items.remove(instance)

    def index(self, instance):
        return self._items.index(instance)

    def __getitem__(self, key):
        return self._items[key]