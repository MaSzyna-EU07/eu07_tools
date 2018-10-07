from typing import Any, Iterable

from . import writers
from eu07_tools.structs.t3d import T3DSubmodel


class T3DDumper:
    def __init__(self, file):
        self._file = file

    # public:
    def dump_submodel(self, submodel: T3DSubmodel):
        writer = writers.get_writer(submodel.type)
        writer.write_submodel(submodel, self._file)

    def dump_include(self, params: Iterable[Any]):
        params_str = (str(p) for p in params)

        self._file.write(
            f"include {' '.join(params_str)} end\n\n"
        )
    
    