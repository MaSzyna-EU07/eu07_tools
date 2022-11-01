from .structures import create_material, Material
from .common import NESTED_MAPPING_KEYS, NUMERIC_KEYS
from eu07_tools.utils import TextScanner


def load(file):
    scanner = TextScanner.from_file(file)
    return _load_material(scanner)


def _load_material(scanner):
    mat = Material()

    while True:
        token = scanner.read_string()
        key = token.rstrip(":")

        if not token:
            break
        elif key == "{":
            continue
        elif key == "}":
            break

        elif "texture" in key:
            token = scanner.read_string()

            if token == "[":
                paths = list(scanner.read_strings_before("]"))
                mat.set_textureset(key, paths)
            else:
                mat.set_texture_path(key, scanner.read_string())

        elif key in NESTED_MAPPING_KEYS:
            mat_variant = _load_material(scanner)
            mat.set_variant(key, mat_variant)

        elif key == "shader":
            mat.shader = scanner.read_string()

        elif key == "opacity":
            mat.opacity = scanner.read_int()

        elif key == "selfillum":
            mat.selfillum = scanner.read_float()

        elif key == "size":
            mat.size = scanner.read_floats(2)

        elif key == "shadow_rank":
            mat.shadow_rank = scanner.read_int()

        elif key.startswith("param"):
            values = []
            while 1:
                token = scanner.read_string()
                try:
                    pv = float(token)
                except ValueError:
                    scanner.put_back(token)
                    break
                else:
                    values.append(pv)

            mat.shader_params[key] = values

    return mat