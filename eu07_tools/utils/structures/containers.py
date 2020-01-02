import collections

class FactorySequence(collections.abc.Sequence):
    def __init__(self, factory, initial_list=None):
        self.factory = factory
        self._items = [] if initial_list is None else initial_list

    def new(self, *args):
        instance = self.factory(*args)
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

class OwnedFactorySequence(FactorySequence):
    def __init__(self, factory, initial_list=None, owner=None):
        super().__init__(factory, initial_list)
        self.owner = owner

    def new(self, *args):
        instance = super().new(*args)
        instance.owner = self.owner
        return instance

