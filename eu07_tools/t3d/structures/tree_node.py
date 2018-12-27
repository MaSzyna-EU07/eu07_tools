class T3DTreeNode:
    def __init__(self, type_, name, data):
        self._name = name
        self.type = type_
        if self.type == "submodel":
            self._refs_manager = T3DSubmodelRefsManager(self)
        elif self.type == "include":
            self._refs_manager = T3DObjectRefsManager(self)

        self._data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.data.name = name

class NodeReferences:
    def __init__(self):
        self.owner = None
        self.parent = None
        self.next = None
        self.first_child = None
        self.last_child = None

    @property
    def children(self):
        current = self.first_child
        while current is not None:
            yield current
            current = current.next

    def append_child(self, new_child):
        if self.first_child is None:
            self.first_child = new_child
            self.last_child = new_child
        else:
            self.last_child.next = new_child
            self.last_child = new_child

        new_child.parent = self.owner


    def remove_child(self, child_to_remove):
        prev = None
        for current in self.children:
            if current is child_to_remove:
                prev.next = current.next
                current.parent = None
                del current
                return
            prev = current

    def insert_after(self, child, ref_child):
        for current in self.owner.children:
            if current is ref_child:
                child.next = current.next
                current.next = child

        child.parent = self.owner


class T3DSubmodelRefsManager(T3DObjectRefsManager):
    def append_child(self, new_child):
        super().append_child(new_child)
        self._set_data_parent_name()

    def remove_child(self, child_to_remove):
        super().remove_child(child_to_remove)
        self._set_data_parent_name()

    def insert_after(self, child, ref_child):
        super().insert_after(child, ref_child)
        self._set_data_parent_name()

    def _set_data_parent_name(self):
        self.owner.data.parent_name = (
            "none" if self.owner.parent is None else self.owner.parent.name
        )