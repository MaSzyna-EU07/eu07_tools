from eu07_tools.io.t3d.dump.dumper import T3DDumper
from eu07_tools.structs.t3d import create_submodel

from unittest import mock

from io import StringIO



class Test_T3DDumper:
    def setup(self):
        self.file = StringIO(newline="\n")
        self.dumper = T3DDumper(self.file)

    def test_dump_include(self):
        self.dumper.dump_include(["some/file.t3d", "param1", "param2", "param3"])

        expected = "include some/file.t3d param1 param2 param3 end\n\n"

        assert self.file.getvalue() == expected

    def test_dump_mesh(self):
        submodel = create_submodel("example", "Mesh")
        submodel.add_triangle(
            [[1, 2, 3, 4, 5]] * 3, smooth=16
        )
        submodel.add_triangle(
            [[1, 2, 3, 4, 5, 6, 7, 8]] * 3, smooth=-1
        )

        self.dumper.dump_submodel(submodel)

        expected = (
            "//---------------------------------------------------------------------------------\n"
            "Parent: none\n"
            "Type: Mesh\n"
            "Name: example\n"
            "Anim: false\n"
            "Ambient: 255 255 255\n"
            "Diffuse: 255 255 255\n"
            "Specular: 255 255 255\n"
            "SelfIllum: 1\n"
            "Wire: false\n"
            "WireSize: 1\n"
            "Opacity: 100\n"
            "Map: none\n"
            "MaxDistance: 1000\n"
            "MinDistance: 0\n"
            "Transform: \n"
            "\t1 0 0 0\n"
            "\t0 1 0 0\n"
            "\t0 0 1 0\n"
            "\t0 0 0 1\n"
            "NumVerts: 6\n"
            "16\n"
            "1 2 3 4 5\n"
            "1 2 3 4 5\n"
            "1 2 3 4 5\n"
            "\n"
            "-1\n"
            "1 2 3 4 5 6 7 8\n"
            "1 2 3 4 5 6 7 8\n"
            "1 2 3 4 5 6 7 8\n"
            "\n"
        )

        assert self.file.getvalue() == expected

    def test_dump_spot(self):
        submodel = create_submodel("example", "FreeSpotLight")

        self.dumper.dump_submodel(submodel)

        expected = (
            "//---------------------------------------------------------------------------------\n"
            "Parent: none\n"
            "Type: FreeSpotLight\n"
            "Name: example\n"
            "Anim: false\n"
            "Diffuse: 255 255 255\n"
            "SelfIllum: 1\n"
            "NearAttenStart: 40\n"
            "NearAttenEnd: 0\n"
            "UseNearAtten: false\n"
            "FarAttenDecayType: 1\n"
            "FarDecayRadius: 45\n"
            "FalloffAngle: 45\n"
            "HotspotAngle: 45\n"
            "MaxDistance: 1000\n"
            "MinDistance: 0\n"
            "Transform: \n"
            "\t1 0 0 0\n"
            "\t0 1 0 0\n"
            "\t0 0 1 0\n"
            "\t0 0 0 1\n"
            "\n"
        )
        assert self.file.getvalue() == expected

    def test_dump_stars(self):
        submodel = create_submodel("example", "Stars")
        submodel.add_star((1, 2, 3), (255, 255, 255))
        submodel.add_star((1, 2, 3), (0, 0, 0))
        submodel.add_star((1, 2, 3), (128, 128, 128))
        submodel.add_star((1, 2, 3), (0, 128, 255))
        submodel.add_star((1, 2, 3), (67, 24, 1))

        self.dumper.dump_submodel(submodel)

        expected = (
            "//---------------------------------------------------------------------------------\n"
            "Parent: none\n"
            "Type: Stars\n"
            "Name: example\n"
            "Anim: false\n"
            "Diffuse: 255 255 255\n"
            "SelfIllum: 1\n"
            "MaxDistance: 1000\n"
            "MinDistance: 0\n"
            "Transform: \n"
            "\t1 0 0 0\n"
            "\t0 1 0 0\n"
            "\t0 0 1 0\n"
            "\t0 0 0 1\n"
            "NumVerts: 5\n"
            "1\n"
            "1 2 3 4278189825 0\n"
            "1 2 3 0 0\n"
            "1 2 3 2147483520 0\n"
            "\n"
            "1\n"
            "1 2 3 4269768704 0\n"
            "1 2 3 16771773 0\n"
            "\n"
        )
        assert self.file.getvalue() == expected


