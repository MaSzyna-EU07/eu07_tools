from eu07_tools.io.t3d.dump.dumper import T3DDumper
from eu07_tools.structs.t3d import T3DMeshSubmodel

from unittest import mock

from io import StringIO

file = StringIO(newline="\n")
dumper = T3DDumper(file)


def test_dump_include():
    dumper.dump_include(["some/file.t3d", "param1", "param2", "param3"])

    expected = "include some/file.t3d param1 param2 param3 end\n\n"

    assert file.getvalue() == expected


def test_dump_submodel():
    submodel = T3DMeshSubmodel("lol")

    assert submodel.name == "lol"