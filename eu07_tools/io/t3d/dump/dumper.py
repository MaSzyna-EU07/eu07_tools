from . import writers

class T3DDumper:
    def __init__(self, file):
        self._file = file
        self._recent_entry_type = ""

    # public:
    def dump_submodel(self, submodel: T3DSubmodel):
        writer = writers.get_writer(submodel.type)
        writer.write_submodel(submodel, self._file)

    def dump_include(self, params: Iterable[Any]):
        self._file.write(
            f"include {" ".join(params)} end\n\n"
        )
    
    