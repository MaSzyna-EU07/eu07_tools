from . import writers


class T3DOutput:
    @classmethod
    def to_file(cls, file):
        return cls(file)

    def __init__(self, file):
        self._file = file

    def dump_from_iterable(self, iterable):
        for element in iterable:
            if element.element_type == "submodel":
                self.dump_submodel(element)
            elif element.element_type == "include":
                self.dump_include(element)

    # public:
    def dump_submodel(self, submodel):
        writer = writers.get_writer(submodel.submodel_type)
        writer.write_submodel(submodel, self._file)

    def dump_include(self, include):
        self._file.write(
            f"include {include.path} end\n\n"
        )
    
    