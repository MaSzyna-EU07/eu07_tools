from eu07_tools.io.mat.load import MATLoader
from ..utils import make_fake_file


class Test_MATLoader:
    def setup(self):
        self.loader = MATLoader()

    def test_load_mat(self):
        file = make_fake_file(
            "texture1: example/tex\n"
            "texture2: [ tex1 tex2 tex3 ]\n"
            "winter: {\n"
            "\ttexture1: example/winter/tex\n"
            "\ttexture2: example/winter/tex_normal\n"
            "}\n"
            "opacity: 0\n"
            "size: 4 5\n"
        )

        material = self.loader.load_from_file(file)

        expected = {
            "texture1": "example/tex",
            "texture2": set(("tex1", "tex2", "tex3")),
            "winter": {
                "texture1": "example/winter/tex",
                "texture2": "example/winter/tex_normal"
            },
            "opacity": 0,
            "size": [4, 5]
        }

        print(material)

        assert material == expected