from io import StringIO

from eu07_tools.io.mat.dump import MATDumper


class Test_MATDumper:
    def setup(self):
        self.file = StringIO()
        self.dumper = MATDumper(self.file)

    def test_dump_material_dict(self):
        material = {
            "texture1": "foo/bar",
            "texture2": ["foo/bar_normal1", "foo/bar_normal2"],
            "winter": {
                "texture1": "winter/tex1",
                "texture2": "winter/tex1_normal"
            },
            "opacity": 0,
            "size": [3, 4]
        }

        expected = (
            "texture1: foo/bar\n"
            "texture2: [ foo/bar_normal1 foo/bar_normal2 ]\n"
            "winter: {\n"
            "\ttexture1: winter/tex1\n"
            "\ttexture2: winter/tex1_normal\n"
            "}\n"
            "opacity: 0\n"
            "size: 3 4\n"
        )

        self.dumper.dump_material_dict(material)
        print(self.file.getvalue())

        assert self.file.getvalue() == expected