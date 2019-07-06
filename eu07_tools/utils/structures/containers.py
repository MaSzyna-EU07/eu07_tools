import collections

class IndexedFactoryContainer(collections.abc.Sequence):
    def __init__(self, cls):
        self.cls = cls
        self._items = []

    def new(self, *args):
        instance = self.cls(args)
        self._items.append(instance)
        return instance

    def remove(self, instance):
        self._items.remove(instance)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)
