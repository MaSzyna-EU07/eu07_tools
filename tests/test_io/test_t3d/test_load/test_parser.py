from eu07_tools.io.t3d.load.parser import T3DPropertiesParser
from ...utils import make_fake_file

class Test_T3DPropertiesParser:
    def setup(self):
        self._parser = T3DPropertiesParser()

    def test_parsing_include(self):
        file = make_fake_file(
            "include some/model.t3d foo bar 1 2 3 end\n"
        )

        parsed = list(self._parser.parse_properties(file))

        expected = [
            ("include", ["some/model.t3d", "foo", "bar", "1", "2", "3"])
        ]

        assert parsed == expected

    def test_parsing_single_value(self):
        file = make_fake_file(
            "Parent: dupa\n"
            "Name: kupa\n"
            "Type: Mesh\n"
            "Anim: false\n"
        )

        parsed = list(self._parser.parse_properties(file))

        expected = [
            ("parent", "dupa"),
            ("name", "kupa"),
            ("type", "Mesh"),
            ("anim", "false")
        ]

        assert parsed == expected

    def test_parsing_rgb(self):
        file = make_fake_file(
            "Ambient: 255 255 255\n"
            "Diffuse: 0 0 0\n"
            "Specular: 128 128 128\n"
        )

        parsed = list(self._parser.parse_properties(file))

        expected = [
            ("ambient", ["255", "255", "255"]),
            ("diffuse", ["0", "0", "0"]),
            ("specular", ["128", "128", "128"])
        ]

        assert parsed == expected

    def test_parsing_matrix(self):
        file = make_fake_file(
            "Transform:\n"
            "\t1 2 3 4\n"
            "\t5 6 7 8\n"
            "\t9 10 11 12\n"
            "\t13 14 15 16\n"
        )

        parsed = list(self._parser.parse_properties(file))

        expected = [
            ("transform", [
            "1", "2", "3", "4", 
            "5", "6", "7", "8", 
            "9", "10", "11", "12", 
            "13", "14", "15", "16"
            ])
        ]

        assert parsed == expected

    def test_parsing_geometry_with_numverts_divisible_by_3(self):
        file = make_fake_file(
            "NumVerts: 6\n"
            "0\n"
            "1 2 3 4 5\n"
            "1 2 3 4 5\n"
            "1 2 3 4 5\n"
            "\n"
            "-1\n"
            "1 2 3 4 5 6 7 8\n"
            "1 2 3 4 5 6 7 8\n"
            "1 2 3 4 5 6 7 8\n"
        )

        parsed = list(self._parser.parse_properties(file))

        expected = [
            ("numverts", "6"),
            ("geometry", [
                [
                    "0", 
                    ["1", "2", "3", "4", "5"],
                    ["1", "2", "3", "4", "5"],
                    ["1", "2", "3", "4", "5"]
                ],
                [
                    "-1", 
                    ["1", "2", "3", "4", "5", "6", "7", "8"],
                    ["1", "2", "3", "4", "5", "6", "7", "8"],
                    ["1", "2", "3", "4", "5", "6", "7", "8"]
                ],
            ])
        ]

        assert parsed == expected

    def test_parsing_geometry_with_numverts_non_divisible_by_3(self):
            file = make_fake_file(
                "NumVerts: 2\n"
                "0\n"
                "1 2 3 4 5\n"
                "1 2 3 4 5\n"
            )

            parsed = list(self._parser.parse_properties(file))

            expected = [
                ("numverts", "2"),
                ("geometry", [
                    [
                        "0", 
                        ["1", "2", "3", "4", "5"],
                        ["1", "2", "3", "4", "5"],
                    ],
                ])
            ]

            assert parsed == expected