import collections

class FactorySequence(collections.abc.Sequence):
    def __init__(self, cls, initial_list=None):
        self.cls = cls
        self._items = [] if initial_list is None else initial_list

    def new(self, *args):
        instance = self.cls(*args)
        self._items.append(instance)
        return instance

    def remove(self, instance):
        self._items.remove(instance)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):
        return self._items == list(other)

class TypedSequenceWrapper(collections.abc.MutableSequence):
    def __init__(self, cls, initial_list=None):
        self.cls = cls
        self._items = [] if initial_list is None else initial_list

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, item):
        self._items[index] = self.cls(item)

    def __delitem__(self, item):
        self._items.remove(item)

    def __len__(self):
        return len(self._items)

    def insert(self, index, item):
        self._items.insert(index, item)
