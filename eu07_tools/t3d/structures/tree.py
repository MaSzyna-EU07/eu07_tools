from .datablocks import create_submodel, create_include, T3DSubmodel

class T3DModelTree:
    def __init__(self):
        self.root_level = T3DTreeNode("submodel", "none", None)

    @classmethod
    def from_file(cls, file):
        pass
        
    def to_file(self, file):
        pass

    def create_submodel(self, type_, name):
        data = create_submodel(type_, name)
        node = T3DTreeNode("submodel", name, data)
        return node

    def create_include(self, name, path):
        data = create_include(path)
        node = T3DTreeNode("include", name, data)
        return node

    def remove_node(self, node, new_children_owner):
        for current in self.objects:
            if current is node:
                node.owner.remove_child(node)
                del node

            if new_children_owner is not None:
                for child in node:
                    new_children_owner.append_child(child)

    def get_submodel(self, name: str):
        if name == "none":
            return self.root_level

        for submodel in self.submodels:
            if submodel.name == name:
                return submodel

    @property
    def root(self):
        return self.root_level.first_child 

    @property
    def nodes(self):
        yield from _traverse_tree_from_root(self.root_level)

    @property
    def submodels(self):
        yield from (node for node in self.nodes if node.type == "submodel")

    @property
    def includes(self):
        yield from (node for node in self.nodes if node.type == "include")

def _traverse_tree_from_root(root):
    yield root
    for child in root.children:
        yield from _traverse_tree_from_root(child)


